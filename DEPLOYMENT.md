# Route implementation and deployment

The project is a downloaded HTML export, not an executable WordPress installation. No build dependencies are needed. The original HTML, CSS layout rules, content, images, and animations are retained; only paths, routing, canonical URLs, malformed prefetch JSON, and backend integration guards were changed. No source pages were moved, deleted, or replaced with mockups.

## Entry points

| URL | Existing source |
| --- | --- |
| `/` | `index.htm` |
| `/spectrum/` | `spectrum-tv/index.htm` |
| `/xfinity/` | `xfinity/index.html` |

Spectrum assets stay at `/spectrum-tv/`; absolute paths allow its page to be served at `/spectrum/` without duplicating it. Old Spectrum entry URLs redirect permanently. Old Xfinity `.htm` and `.html` entry links resolve to `/xfinity/`. Each of the three pages has exactly one absolute canonical for its intended production URL. Existing titles and descriptions remain intact. Provider home links stay within their respective provider site.

## Files changed or added

- `.htaccess`: Apache/LiteSpeed directory entry order, Spectrum rewrite, legacy redirects, CSS content type for downloaded extensionless font stylesheets. No WordPress catch-all is introduced.
- `vercel.json`: equivalent static rewrites, redirects, MIME headers, and buildless deployment settings.
- `.vercelignore`: excludes development helpers and reports from Vercel deployment.
- `index.htm`, `spectrum-tv/index.htm`, `xfinity/index.html`: route/asset paths, canonical URLs, and the integration corrections below.
- Main-site HTML pages in `about-us/`, `att/`, `contact-us/`, `customer-service/`, `directv/`, `earthlink/`, `get-a-new-connection/`, `internet-packages/`, `privacy-policy/`, `switch-your-tv-internet-service/`, `t_n_c/`, `tv-internet-services/`, and `tv-packages/`: local paths for available original assets, corrected provider navigation where present, and the static cache guard.
- `spectrum-tv/css`: missing Open Sans references now point to their original `fonts.gstatic.com` URLs.
- `ajax/` and `signals/`: missing shared assets recovered from the adjacent existing `cabletvasisst.com` download, without replacing any existing files.
- Missing original assets under `wp-content/` and `wp-includes/js/` were restored from `https://tvinternetpackage.com`. See `asset-restoration.json` for individual files and unavailable resources. Existing asset files were not overwritten.
- `tools/serve.py`, `tools/check-routes.py`, `tools/check-browser.mjs`: local preview and verification helpers.
- `browser-check.json`, `route-check.json`: actual test results.

## Local commands

From the project root:

```sh
python3 tools/serve.py
```

Open `http://127.0.0.1:8080/`, `/spectrum/`, and `/xfinity/`.
In another terminal:

```sh
python3 tools/check-routes.py
```

This crawls internal navigation and recursively referenced CSS assets. It currently exits nonzero for one original image unavailable both locally and on the original server: `/wp-content/themes/nestnet/assets/img/img-after.png`. Restore that exact original file from a backup to resolve the remaining audit failure. No substitute image was introduced.

For browser checks, Node 24 and Chrome are used; no npm installation is needed:

```sh
google-chrome --headless --no-sandbox --disable-gpu --remote-debugging-port=9222 --user-data-dir=/tmp/tv-route-chrome about:blank
node tools/check-browser.mjs
```

Only use this Chrome command for the local test browser. The check loads all three pages, triggers delayed JavaScript and lazy images, checks canonical tags and image loading, and clicks both provider mobile menu controls.

Results: all three pages rendered with zero uncaught JavaScript exceptions and zero broken rendered images. Both provider mobile menu controls toggled successfully. The recursive HTTP audit checked 205 URLs and found the single original missing image above. Existing Google advertising requests were aborted in the local browser; provider pages had no failed requests. There are 148 existing `href="#"` placeholder links across the crawled pages; their content/behavior was preserved. This is not a verification of backend form submission or every possible interaction. Apache/LiteSpeed and Vercel runtime routing must also be smoke-tested in staging; the local server reproduces the route map but does not execute either hosting engine or PHP.

## Backend dependencies retained

- There is no `wp-config.php`, executable WordPress core, database backup, `wp-admin`, or working local REST/AJAX backend. `xmlrpc.php` contains a downloaded XML discovery document, not the WordPress PHP service. `wp-json/` contains snapshots, not an API implementation.
- The contact page uses Contact Form 7 and still needs its real WordPress REST endpoints, plugin, database, mail configuration, and server validation. Other embedded WordPress/Elementor/WooCommerce AJAX configuration is preserved. Do not treat an HTTP 200 from a downloaded REST snapshot as a working backend. No forms were submitted during testing.
- The provider exports have no active qualification forms: Xfinity's form is commented out and Spectrum's modal body is empty. Xfinity's qualification script now loads only when the genuine `window.updater_qualform` configuration is supplied by its backend. Its original script file remains in place. Address qualification depends on Updater/Smarty services and genuine configuration; no dummy credentials or success responses were added.
- LiteSpeed's guest cache variation request previously POSTed to an absent PHP file and threw a JSON parsing error on static hosting. It now runs only when `window.TV_INTERNET_WORDPRESS_BACKEND = true` is explicitly set before the original cache script. Enable this only after restoring that real backend. This affects server cache variation, not client animations or layout.
- Original external fonts, analytics, advertising, and monitoring services remain external dependencies. Secondary REST metadata links and the absent privacy-policy feed are original export limitations.

## Hostinger deployment

Upload the website files and asset directories into the domain's `public_html`, including the new `.htaccess`. Do not upload `tools/`, test JSON reports, or local metadata directories. Keep the exact folder names. No new `index.html` copy is required: `DirectoryIndex` serves `index.htm`, and the Spectrum rewrite serves its existing source page. An Apache-compatible/LiteSpeed host with rewrite support is required.

If production already contains WordPress or its own `.htaccess`, merge these route rules with that configuration in staging first; place the specific provider rules before the WordPress front-controller rules. Do not replace the live WordPress installation, its `xmlrpc.php`, or its database with downloaded snapshots. A complete WordPress backup is needed if dynamic forms/API features must run on this host. The new local configuration does not supply WordPress functionality.

Hostinger reference: https://www.hostinger.com/support/how-to-upload-a-website-from-backups/

## Vercel deployment

Import this directory as a project with Framework Preset **Other**. The included `vercel.json` sets no build command and uses `.` as the output directory. Keep `vercel.json` at the deployment root and deploy all assets together. Vercel uses that JSON configuration, not `.htaccess`. There is no SPA fallback: missing assets correctly return 404 rather than the main page.

This deployment serves the static pages only. The absent WordPress/PHP backend cannot be restored by these rewrites; keep a real backend on PHP hosting and deliberately configure its supported endpoints/CORS if dynamic features are required. Do not proxy submissions to a static snapshot.

Vercel references: https://vercel.com/docs/builds/configure-a-build and https://vercel.com/docs/project-configuration/vercel-json

After either staging deployment, verify the three routes, provider mobile navigation, CSS/font response types, legacy redirects, one canonical per page, and any real backend submissions with test data. DNS and production hosting settings were not changed, and no deployment was performed.
