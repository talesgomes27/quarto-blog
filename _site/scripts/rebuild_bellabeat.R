#!/usr/bin/env Rscript
# Rebuild the corrected descriptive study from the pinned public ZIP; no download or package installation.
args <- commandArgs(trailingOnly = TRUE)
options(warn = 1)
if (length(args) != 1L) stop("Usage: Rscript --vanilla scripts/rebuild_bellabeat.R /path/to/source.zip")
required <- c("data.table", "dplyr", "ggplot2", "jsonlite", "digest")
for (pkg in required) if (!requireNamespace(pkg, quietly = TRUE)) stop("Missing installed package: ", pkg)
suppressPackageStartupMessages({ library(dplyr); library(ggplot2) })
script_arg <- grep("^--file=", commandArgs(), value = TRUE)
script_path <- normalizePath(sub("^--file=", "", script_arg[[1]]))
root <- dirname(dirname(script_path))
output <- file.path(root, "posts/bellabeat/revision-2026-10-26")
dir.create(output, recursive = TRUE, showWarnings = FALSE)
source_zip <- normalizePath(args[[1]], mustWork = TRUE)
expected_md5 <- "7afbecdce29814e1be2e9a7c94f8f165"
expected_sha256 <- "4741dfabd18453de19b6dd0a7204e8fea6e45e70bc9ddbe396956c8e4fde02f8"
sha256 <- function(path) digest::digest(file = path, algo = "sha256")
stopifnot(unname(tools::md5sum(source_zip)) == expected_md5, sha256(source_zip) == expected_sha256)
basenames <- c("dailyActivity_merged.csv", "sleepDay_merged.csv", "heartrate_seconds_merged.csv", "weightLogInfo_merged.csv")
members <- unzip(source_zip, list = TRUE)$Name
selected <- vapply(basenames, function(name) {
  hit <- members[basename(members) == name]
  stopifnot(length(hit) == 1L, !grepl("(^/|\\\\|(^|/)\\.\\.(/|$))", hit))
  hit
}, character(1))
temporary <- tempfile("bellabeat-")
dir.create(temporary)
unzip(source_zip, files = unname(selected), exdir = temporary)
read_source <- function(name) data.table::fread(file.path(temporary, selected[[name]]), colClasses = c(Id = "character"))
date_only <- function(value) as.Date(sub(" .*", "", value), format = "%m/%d/%Y")
check_key <- function(data) stopifnot(!anyNA(data[c("Id", "date")]), !anyDuplicated(data[c("Id", "date")]))

activity_raw <- read_source("dailyActivity_merged.csv")
sleep_raw <- read_source("sleepDay_merged.csv")
weight_raw <- read_source("weightLogInfo_merged.csv")
heart_raw <- read_source("heartrate_seconds_merged.csv")
input_counts <- list(activity = nrow(activity_raw), sleep = nrow(sleep_raw), heart_samples = nrow(heart_raw), weight = nrow(weight_raw))
sleep <- unique(sleep_raw)
stopifnot(nrow(sleep_raw) - nrow(sleep) == 3L)
activity <- as.data.frame(activity_raw) |>
  transmute(Id, date = date_only(ActivityDate), total_steps = TotalSteps, total_distance = TotalDistance,
    calories = Calories, sedentary_time = SedentaryMinutes / 60,
    lightly_active_time = LightlyActiveMinutes / 60, fairly_active_time = FairlyActiveMinutes / 60,
    very_active_time = VeryActiveMinutes / 60, sedentary_distance = SedentaryActiveDistance,
    lightly_active_distance = LightActiveDistance, fairly_active_distance = ModeratelyActiveDistance,
    very_active_distance = VeryActiveDistance)
sleep <- as.data.frame(sleep) |>
  transmute(Id, date = date_only(SleepDay), total_time_asleep = TotalMinutesAsleep / 60,
    total_time_in_bed = TotalTimeInBed / 60, awake_time_in_bed = (TotalTimeInBed - TotalMinutesAsleep) / 60)
weight <- as.data.frame(weight_raw) |> transmute(Id, date = date_only(Date), weight_kg = WeightKg, bmi = BMI)
heart_raw[, date := date_only(Time)]
heart <- as.data.frame(heart_raw[, .(heartrate = mean(Value)), by = .(Id, date)])
for (table in list(activity, sleep, heart, weight)) check_key(table)
stopifnot(nrow(activity) == 940L, n_distinct(activity$Id) == 33L,
  nrow(sleep) == 410L, n_distinct(sleep$Id) == 24L,
  nrow(heart) == 334L, n_distinct(heart$Id) == 14L,
  nrow(weight) == 67L, n_distinct(weight$Id) == 8L,
  !anyNA(activity), !anyNA(sleep$date), !anyNA(heart$heartrate))
daily <- activity |>
  left_join(heart, by = c("Id", "date"), relationship = "one-to-one") |>
  left_join(sleep, by = c("Id", "date"), relationship = "one-to-one") |>
  left_join(weight, by = c("Id", "date"), relationship = "one-to-one") |>
  mutate(weekday = as.integer(format(date, "%u")), sleep_group = case_when(
    is.na(total_time_asleep) ~ NA_character_, total_time_asleep < 6 ~ "lt6",
    total_time_asleep <= 10 ~ "6to10", TRUE ~ "gt10"))
check_key(daily)
stopifnot(nrow(daily) == 940L, sum(!is.na(daily$total_time_asleep)) == 410L,
  sum(!is.na(daily$heartrate)) == 334L, sum(!is.na(daily$bmi)) == 67L,
  abs(mean(daily$total_steps) - 7637.91063829787) < 1e-7,
  abs(mean(daily$calories) - 2303.60957446809) < 1e-7,
  min(daily$date) == as.Date("2016-04-12"), max(daily$date) == as.Date("2016-05-12"))

intensities <- c("sedentary", "lightly_active", "fairly_active", "very_active")
long <- bind_rows(lapply(intensities, function(intensity) {
  data.frame(Id = daily$Id, date = daily$date, weekday = daily$weekday,
    intensity = intensity, hours = daily[[paste0(intensity, "_time")]],
    distance_km = daily[[paste0(intensity, "_distance")]],
    calories = daily$calories, steps = daily$total_steps)
}))
stopifnot(nrow(long) == 3760L, !anyDuplicated(long[c("Id", "date", "intensity")]))
summarize_field <- function(data, field) {
  usable <- data[!is.na(data[[field]]), , drop = FALSE]
  values <- usable[[field]]
  list(observations = length(values), users = n_distinct(usable$Id), missing = nrow(data) - length(values),
    mean = mean(values), median = median(values), q25 = unname(quantile(values, .25)),
    q75 = unname(quantile(values, .75)), min = min(values), max = max(values))
}
fields <- c("total_steps", "total_distance", "calories", "heartrate", "bmi", "total_time_asleep",
  "sedentary_time", "total_time_in_bed", "awake_time_in_bed")
summary <- setNames(lapply(fields, function(field) summarize_field(daily, field)), fields)
weekday <- daily |> group_by(weekday) |> summarise(observations = n(), users = n_distinct(Id),
  dates = n_distinct(date), mean_distance_km = mean(total_distance), mean_steps = mean(total_steps), .groups = "drop")
sleep_groups <- setNames(lapply(c("lt6", "6to10", "gt10"), function(group) {
  data <- daily[daily$sleep_group == group & !is.na(daily$sleep_group), ]
  list(observations = nrow(data), users = n_distinct(data$Id),
    heartrate = summarize_field(data, "heartrate"), calories = summarize_field(data, "calories"),
    total_steps = summarize_field(data, "total_steps"))
}), c("lt6", "6to10", "gt10"))
historical_path <- file.path(root, "docs/reviews/evidence/bellabeat-audit.json")
historical <- jsonlite::fromJSON(historical_path, simplifyVector = FALSE)
results <- list(revision = "2026-10-26", analysis = "Corrected descriptive Bellabeat case study; original upstream Fitbit records",
  period = c(start = as.character(min(daily$date)), end = as.character(max(daily$date))),
  rows = nrow(daily), users = n_distinct(daily$Id), unique_user_days = nrow(unique(daily[c("Id", "date")])),
  input_rows = input_counts, removed_exact_sleep_duplicates = 3L, long_rows = nrow(long),
  summary = summary, weekday = weekday, sleep_groups = sleep_groups,
  historical_comparison = list(rows = historical$rows, summary = historical$archived_summary),
  interpretation = list(unit = "Available participant-day records, not independent participants",
    zero_policy = "Zero values and missing auxiliary measurements retained; no inferred non-wear filter",
    heart_rate = "Arithmetic mean of available measurements per day, not resting heart rate",
    causal = "Descriptive associations only; no clinical outcome or causal effect estimated"))
jsonlite::write_json(results, file.path(output, "results.json"), pretty = TRUE, auto_unbox = TRUE, digits = NA, na = "null")

labels <- list(
  pt = list(days = c("Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"),
    intensity = c("Sedentária", "Leve", "Moderada", "Intensa"), sleep = c("<6 horas", "6–10 horas", ">10 horas"),
    title_weekday = "Distância média registrada por dia da semana", distance = "Distância total registrada (km/dia)",
    intensity_distance = "Distância por intensidade (km/dia)",
    hours = "Tempo registrado (h/dia)", steps = "Passos registrados por dia", calories = "Gasto energético total estimado (kcal/dia)",
    time_distance = "Tempo e distância por intensidade", time_calories = "Tempo por intensidade e gasto energético",
    time_steps = "Tempo por intensidade e passos diários", sleep_calories = "Passos e gasto energético por faixa de sono",
    sleep_heart = "FC média diária observada por faixa de sono", heart = "Média diária das medições de FC (bpm)",
    note = "Registros de participante-dia; medidas repetidas. Comparação descritiva, sem inferência causal.",
    counts = "registros / IDs", dates = "datas", source = "Fonte: Fitbit / Zenodo · 12/04–12/05/2016 · revisão 26/10/2026"),
  en = list(days = c("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"),
    intensity = c("Sedentary", "Light", "Moderate", "Vigorous"), sleep = c("<6 hours", "6–10 hours", ">10 hours"),
    title_weekday = "Mean recorded distance by weekday", distance = "Total recorded distance (km/day)",
    intensity_distance = "Distance by intensity (km/day)",
    hours = "Recorded time (hours/day)", steps = "Recorded steps per day", calories = "Estimated total energy expenditure (kcal/day)",
    time_distance = "Time and distance by intensity", time_calories = "Time by intensity and energy expenditure",
    time_steps = "Time by intensity and daily steps", sleep_calories = "Steps and energy expenditure by sleep duration",
    sleep_heart = "Observed mean daily heart rate by sleep duration", heart = "Daily mean of heart-rate readings (bpm)",
    note = "Participant-day records; repeated measurements. Descriptive comparison, no causal inference.",
    counts = "records / IDs", dates = "dates", source = "Source: Fitbit / Zenodo · Apr 12–May 12, 2016 · revised Oct 26, 2026"))
palette <- c("#6a7c87", "#619c91", "#136c65", "#172f3f")
theme_set(theme_minimal(base_size = 13, base_family = "sans") + theme(
  plot.title = element_text(face = "bold", size = 17, color = "#172f3f"),
  plot.subtitle = element_text(size = 11, color = "#4c6170"),
  plot.caption = element_text(size = 9, hjust = 0, color = "#4c6170", lineheight = 1.15),
  panel.grid.minor = element_blank(), strip.text = element_text(face = "bold"), legend.position = "none",
  plot.margin = margin(12, 16, 12, 12)))
write_table <- function(header, rows, path) {
  lines <- c(paste0("| ", paste(header, collapse = " | "), " |"),
    paste0("| ", paste(rep("---", length(header)), collapse = " | "), " |"),
    vapply(rows, function(row) paste0("| ", paste(row, collapse = " | "), " |"), character(1)))
  writeLines(lines, path, useBytes = TRUE)
}
for (lang in names(labels)) {
  lab <- labels[[lang]]
  fmt <- function(value, digits = 2) formatC(value, format = "f", digits = digits,
    decimal.mark = if (lang == "pt") "," else ".", big.mark = if (lang == "pt") "." else ",")
  var_labels <- if (lang == "pt") c("Passos/dia", "Distância total (km/dia)", "Gasto energético total estimado (kcal/dia)",
    "FC média diária (bpm)", "IMC (kg/m²)", "Sono (h/dia)", "Tempo sedentário (h/dia)", "Tempo total na cama (h/dia)", "Tempo acordado na cama (h/dia)") else
    c("Steps/day", "Total distance (km/day)", "Estimated total energy expenditure (kcal/day)", "Mean daily heart rate (bpm)",
      "BMI (kg/m²)", "Sleep (hours/day)", "Sedentary time (hours/day)", "Total time in bed (hours/day)", "Awake time in bed (hours/day)")
  rows <- lapply(seq_along(fields), function(i) {
    stat <- summary[[fields[[i]]]]
    c(var_labels[[i]], stat$observations, stat$users, stat$missing, fmt(stat$mean), fmt(stat$median))
  })
  write_table(if (lang == "pt") c("Variável", "Registros", "IDs", "Ausentes", "Média", "Mediana") else
    c("Variable", "Records", "IDs", "Missing", "Mean", "Median"), rows, file.path(output, paste0("summary-", lang, ".md")))
  rows <- lapply(seq_len(nrow(weekday)), function(i) {
    row <- weekday[i, ]; c(lab$days[[row$weekday]], row$observations, row$users, row$dates, fmt(row$mean_distance_km, 3), fmt(row$mean_steps, 2))
  })
  write_table(if (lang == "pt") c("Dia", "Participantes-dias", "IDs", "Datas", "Distância média (km)", "Passos médios") else
    c("Day", "Participant-days", "IDs", "Dates", "Mean distance (km)", "Mean steps"), rows, file.path(output, paste0("weekday-", lang, ".md")))
  rows <- lapply(seq_along(sleep_groups), function(i) {
    group <- sleep_groups[[i]]; c(lab$sleep[[i]], group$observations, group$users,
      group$heartrate$observations, group$heartrate$users, fmt(group$heartrate$mean))
  })
  write_table(if (lang == "pt") c("Sono", "Registros com sono", "IDs com sono", "Registros com FC", "IDs com FC", "FC média (bpm)") else
    c("Sleep", "Records with sleep", "IDs with sleep", "Records with HR", "IDs with HR", "Mean HR (bpm)"), rows, file.path(output, paste0("sleep-", lang, ".md")))
  rows <- lapply(seq_len(7), function(i) c(var_labels[[i]],
    fmt(historical$archived_summary[[fields[[i]]]]$mean, 4), fmt(summary[[fields[[i]]]]$mean, 4)))
  write_table(if (lang == "pt") c("Variável", "Média histórica (943 linhas)", "Média corrigida (940 linhas)") else
    c("Variable", "Historical mean (943 rows)", "Corrected mean (940 rows)"), rows, file.path(output, paste0("comparison-", lang, ".md")))
  plot_daily <- daily |> mutate(sleep_label = factor(sleep_group, levels = names(sleep_groups), labels = lab$sleep))
  plot_long <- long |> mutate(intensity_label = factor(intensity, levels = intensities, labels = lab$intensity))
  week <- weekday |> mutate(label = paste0(lab$days[weekday], "\nn=", observations, "; ", dates, " ", lab$dates))
  base_caption <- paste(lab$note, lab$source, sep = "\n")
  plots <- list(
    weekday = ggplot(week, aes(x = factor(label, levels = label), y = mean_distance_km)) +
      geom_col(fill = "#136c65", width = .7) + labs(title = lab$title_weekday, x = NULL, y = lab$distance, caption = base_caption),
    intensity_distance = ggplot(plot_long, aes(hours, distance_km, color = intensity_label)) +
      geom_point(alpha = .35, size = 1.05) + facet_wrap(~intensity_label, ncol = 2, scales = "free") +
      scale_color_manual(values = palette) + labs(title = lab$time_distance, x = lab$hours, y = lab$intensity_distance, caption = base_caption),
    intensity_calories = ggplot(plot_long, aes(hours, calories, color = intensity_label)) +
      geom_point(alpha = .35, size = 1.05) + facet_wrap(~intensity_label, ncol = 2, scales = "free_x") +
      scale_color_manual(values = palette) + labs(title = lab$time_calories, x = lab$hours, y = lab$calories, caption = base_caption),
    intensity_steps = ggplot(plot_long, aes(hours, steps, color = intensity_label)) +
      geom_point(alpha = .35, size = 1.05) + facet_wrap(~intensity_label, ncol = 2, scales = "free_x") +
      scale_color_manual(values = palette) + labs(title = lab$time_steps, x = lab$hours, y = lab$steps, caption = base_caption),
    sleep_calories = ggplot(filter(plot_daily, !is.na(sleep_label)), aes(total_steps, calories)) +
      geom_point(color = "#136c65", alpha = .5, size = 1.3) + facet_wrap(~sleep_label, ncol = 3) +
      labs(title = lab$sleep_calories, x = lab$steps, y = lab$calories, caption = base_caption))
  hr_caption <- paste(vapply(seq_along(sleep_groups), function(i) {
    stat <- sleep_groups[[i]]$heartrate
    paste0(lab$sleep[[i]], ": ", stat$observations, "/", stat$users)
  }, character(1)), collapse = "; ")
  plots$sleep_heart <- ggplot(filter(plot_daily, !is.na(sleep_label), !is.na(heartrate)), aes(sleep_label, heartrate)) +
    geom_boxplot(fill = "#d7e8df", color = "#172f3f", outlier.shape = NA, width = .55) +
    geom_point(position = position_jitter(width = .1, height = 0, seed = 20261026), color = "#136c65", alpha = .5, size = 1.25) +
    labs(title = lab$sleep_heart, x = NULL, y = lab$heart,
      caption = paste(lab$counts, hr_caption, base_caption, sep = "\n"))
  for (name in names(plots)) ggsave(file.path(output, paste0(name, "-", lang, ".png")), plots[[name]],
    width = 9, height = if (name == "sleep_heart") 6.3 else 6, dpi = 140, bg = "white", device = grDevices::png, type = "cairo")
}
versions <- setNames(lapply(required, function(pkg) as.character(packageVersion(pkg))), required)
files <- list.files(output, full.names = TRUE)
files <- files[basename(files) != "provenance.json"]
provenance <- list(revision = "2026-10-26", generated_at_utc = format(Sys.time(), tz = "UTC", usetz = TRUE),
  source = list(url = "https://zenodo.org/records/53894/files/mturkfitbit_export_4.12.16-5.12.16.zip",
    md5 = expected_md5, sha256 = expected_sha256, bytes = file.info(source_zip)$size,
    records = input_counts, file_sha256 = setNames(lapply(selected, function(name) sha256(file.path(temporary, name))), basenames)),
  historical_frozen_sha256 = sha256(file.path(root, "_freeze/posts/bellabeat/index/execute-results/html.json")),
  historical_audit_sha256 = sha256(historical_path), script = "scripts/rebuild_bellabeat.R", script_sha256 = sha256(script_path),
  R = R.version.string, graphics_device = "grDevices::png(type = cairo)", package_versions = versions,
  checks = list(activity_unique_user_days = 940L, sleep_removed_exact_duplicates = 3L,
    daily_rows = 940L, long_rows = 3760L, unique_keys_verified = TRUE, raw_ids_exported = FALSE),
  outputs_sha256 = setNames(lapply(files, sha256), basename(files)),
  policy = c("No individual rows or identifiers exported", "No wear-time or zero-value exclusion inferred",
    "Charts show repeated participant-days; no independent-observation CI or causal model",
    "This upstream archive is not proof of binary identity with the author's original Kaggle download"))
jsonlite::write_json(provenance, file.path(output, "provenance.json"), pretty = TRUE, auto_unbox = TRUE, digits = NA)
unlink(temporary, recursive = TRUE)
cat("Corrected Bellabeat: 940 unique participant-days; 33 IDs; 3760 intensity records.\n")
cat("Sleep 410/24 IDs; heart rate 334/14 IDs; BMI 67/8 IDs.\n")
cat("Mean steps:", summary$total_steps$mean, "; calories:", summary$calories$mean, "; sleep hours:", summary$total_time_asleep$mean, "\n")
cat("Outputs:", output, "\n")
