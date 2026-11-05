# Project study pages implementation plan

> **For agentic workers:** Use superpowers:executing-plans for integration and the dispatching-parallel-agents workflow for the independent editorial imports. Checkboxes track verified deliverables.

**Goal:** Publish the four recent projects as PT/EN studies with the same reading features as Bike-share and Bellabeat.

**Architecture:** Import the existing public rendered reports as static Quarto content. Keep immutable source snapshots and figure hashes; translate narrative, captions and table labels without changing numbers or code. Reuse the installed filters, native lightbox and inherited Giscus configuration.

**Tech Stack:** Quarto 1.10.19, Markdown engine, existing Lua filters, Python standard library, Pandoc.

**Spec:** Current user request: include the four projects in Textos e estudos, PT/EN, with comments, citation, image lightbox and existing blog functionality.

## Global constraints

- Exclude the TCC. Keep the two existing studies and their URLs intact.
- Do not execute project analyses or install dependencies/extensions.
- Preserve original report dates; record blog import date and source provenance.
- Use `engine: markdown`, `freeze: false`, `remember`, `cite-this`, `lightbox: true`, author Tales Gomes and equivalent translation links.
- Keep GitHub links and use internal study links from the home and archive.

## Review focus

- No broken translated links or cross-language RSS entries.
- Original figure bytes, numeric table values and displayed code remain verifiable.
- Comments use the existing repository/category and the correct interface language/theme.
- Citations and sharing use the exact local translation URL.
- Tables, equations, figures and citation controls remain usable on mobile and in both themes.

## Tasks

- [x] Archive source QMD/HTML, mirror report figures, create static Markdown and provenance per project under `posts/{ecommerce,sherlock,fraud,youtube}/`.
- [x] Prepare full PT/EN editorial imports, retaining source results/code and adding traceability links and citation shortcode.
- [x] Register four translation pairs in `scripts/localize.py`; extend the two archive listings and change home links to the internal studies.
- [x] Extend existing feature/navigation/extension checks and add source-preservation checks for the new posts; include checks in Pages CI.
- [x] Render the complete site; verify all checks, bilingual feeds, native lightbox, citation, Giscus and responsive themes in the browser.
- [ ] Publish the validated artifact and compare public pages/resources to the local build.
