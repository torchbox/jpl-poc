const browserSync = require("browser-sync");

const bs = browserSync.create("BrowserSync");

function serve(cb) {
  bs.init({
    open: false,
    proxy: "http://localhost:8000",
  });

  cb();
}

module.exports = serve;
