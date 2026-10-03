# HumanFrame public website

This folder is a standalone static export of the HumanFrame Robotics marketing website. It contains no Flask application, authentication flow, database, deployment service, SSH code, upload handler, API route, or Platform runtime.

## Deploy

Publish the contents of this folder as the web root on any static host. There is no build step and there are no runtime dependencies.

For a local preview from the repository root:

```sh
python3 -m http.server 8080 --directory humanframe-website
```

Then open `http://localhost:8080/`.

Directory index support must be enabled so paths such as `/alp/` serve `alp/index.html`. The `_headers` file applies a restrictive security policy on hosts that support the Netlify or Cloudflare Pages headers format. Configure equivalent headers in the host dashboard if `_headers` is not supported.

## Deliberate limitations

- Platform access, login and registration links are not present.
- The contact page does not submit or store data.
- JavaScript is limited to navigation, header state and on-scroll presentation effects.
- All fonts and imagery are served locally.

