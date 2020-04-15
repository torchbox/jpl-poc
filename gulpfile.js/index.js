const { parallel, series } = require("gulp");

const copy = require("./copy");
const images = require("./images");
const { scripts } = require("./scripts");
const serve = require("./serve");
const styles = require("./styles");
const watch = require("./watch");

const build = parallel(styles, scripts, images, copy);
const defaultTask = series(build, serve, watch);

module.exports = {
  build,
  copy,
  images,
  scripts,
  serve,
  styles,
  default: defaultTask,
};
