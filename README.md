![header](brand/header.png)

# Tankōbon

## End of life

Tankōbon has reached its end of life and will no longer receive any updates. For a similar project, checkout [Kaboom](https://github.com/kaboom-db/kaboom) which is Tankōbon's spiritual successor and has support for a wider range of comics.

## What is Tankōbon?

Manga chapters are often split into volumes (think about how TV shows are split into seasons) which is what we call the Tankōbon format, however, so far I haven't found any central place that documents what chapter is in which volume. This hobby project is an attempt to fix that, and make life easier for those who categorise their manga into volumes.

## Linting

Fix linting errors in HTML files:

```bash
djlint .
```

Check linting errors in HTML files:

```bash
djlint --list-fixes .
```

Check linting errors in Python files:

```bash
pylint $(git ls-files '*.py')
```

Fix linting errors in Python files:

```bash
black .
```

Fix linting errors in CSS files:

```bash
npm run lint:styles
```

Fix linting errors in JavaScript files:

```bash
npm run lint:js
```