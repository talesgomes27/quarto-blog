---@diagnostic disable: undefined-global
-- SCRIPT_FILE fica fechado sobre o valor correto de PANDOC_SCRIPT_FILE lido
-- aqui, no topo do chunk deste filtro. Dentro de um `quarto render`, o mesmo
-- nome lido de dentro de um módulo carregado por require (csl.lua, por
-- exemplo) enxerga outro valor: main.lua, o runner de filtros do próprio
-- Quarto — não o arquivo deste filtro. csl.style_dir() depende de
-- PANDOC_SCRIPT_FILE para achar tests/_extensions/cite-this/styles/*.csl, e
-- csl.lua é módulo de tarefa anterior que não pode ser alterado aqui. Por
-- isso collect() reafirma _G.PANDOC_SCRIPT_FILE (a tabela global de fato,
-- não a variável local deste chunk) logo antes de chamar data.get, que é
-- quem aciona csl.resolve_styles.
local SCRIPT_FILE = PANDOC_SCRIPT_FILE
package.path = ((SCRIPT_FILE or ""):match("(.*[/\\])") or "") .. "?.lua;" .. package.path

local data = require("data")
local widget = require("widget")

local state = nil

local function collect(meta)
  local previous_script = _G.PANDOC_SCRIPT_FILE
  _G.PANDOC_SCRIPT_FILE = SCRIPT_FILE
  local ok, result = pcall(data.get, meta)
  _G.PANDOC_SCRIPT_FILE = previous_script
  if not ok then error(result) end
  state = result
  return meta
end

local function inject(doc)
  if not state then return doc end
  local cfg = state.cfg
  if cfg.position == "inline" or cfg.position == "none" then return doc end
  if #state.styles == 0 then return doc end
  if not data.wants_format(cfg) then return doc end
  if not quarto.doc.is_format("html:js") then return doc end

  data.add_dependency()
  doc.blocks:insert(pandoc.RawBlock("html", widget.build(state, { mode = "actions" })))
  return doc
end

return {
  { Meta = collect },
  { Pandoc = inject },
}
