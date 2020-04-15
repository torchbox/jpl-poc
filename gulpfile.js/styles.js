const browserSync = require("browser-sync");
const csso = require("gulp-csso");
const gulpif = require("gulp-if");
const postcss = require("gulp-postcss");
const sass = require("gulp-sass");
const sassGlob = require("gulp-sass-glob");
const sourcemaps = require("gulp-sourcemaps");
const tailwindcss = require("tailwindcss");
const { argv } = require("yargs");
const { dest, src } = require("gulp");

const { plumbing } = require("./utils");
const bs = browserSync.get("BrowserSync");

function styles() {
  const purgecss = require("@fullhuman/postcss-purgecss")({
    content: ["jpl/**/*.html", "static/scripts/**/*.js"],
    defaultExtractor: (content) => content.match(/[\w-/:]+(?<!:)/g) || [],
  });

  return src(["static/styles/**/*.scss"])
    .pipe(plumbing())
    .pipe(sassGlob())
    .pipe(gulpif(!argv.prod, sourcemaps.init()))
    .pipe(
      sass({
        includePaths: ["node_modules"],
      })
    )
    .pipe(postcss([tailwindcss("tailwind.config.js"), require("autoprefixer")]))
    .pipe(gulpif(argv.prod, postcss([purgecss])))
    .pipe(gulpif(argv.prod, csso()))
    .pipe(gulpif(!argv.prod, sourcemaps.write()))
    .pipe(dest("_build/styles/"))
    .pipe(gulpif(!argv.prod, bs.reload({ stream: true })));
}

module.exports = styles;
