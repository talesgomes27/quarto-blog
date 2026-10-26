# Quarto listing runtime

`quarto-listing.js` is an unchanged copy from Quarto 1.10.19, `/opt/quarto/share/projects/website/listing/quarto-listing.js` (https://github.com/quarto-dev/quarto-cli). The post-render hook installs it over the older runtime copied from historical `_freeze/site_libs/`, without modifying the frozen analysis archive. The current renderer encodes category values as base64; the old runtime incorrectly searched the encoded aggregate string and returned no entries.

When upgrading Quarto, update this copy from the same renderer and verify category selection, reset, sort, text filter and PT/EN links in the browser.
