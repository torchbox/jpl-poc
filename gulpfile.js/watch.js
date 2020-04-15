const browserSync = require("browser-sync");
const images = require("./images");
const styles = require("./styles");
const { compiler } = require("./scripts");
const { watch } = require("gulp");

const bs = browserSync.get("BrowserSync");

function reload(done) {
  bs.reload();
  done();
}

function watchTask() {
  const watchOptions = {
    usePolling: true,
  };
  watch("static/styles/**/*.scss", watchOptions, styles);
  watch("static/images/**/*.{jpg,png}", watchOptions, images);
  watch("jpl/**/*.html", watchOptions, reload);

  compiler.watch(
    {
      poll: 500,
    },
    () => {
      bs.reload();
    }
  );
}

module.exports = watchTask;
