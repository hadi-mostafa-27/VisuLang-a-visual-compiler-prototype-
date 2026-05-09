const {
  Presentation,
  PresentationFile,
  column,
  text,
  fill,
  hug,
  fixed,
  rule,
} = await import("@oai/artifact-tool");

const presentation = Presentation.create({
  slideSize: { width: 1920, height: 1080 },
});

const slide = presentation.slides.add();
slide.compose(
  column(
    { name: "root", width: fill, height: fill, padding: 96, gap: 28 },
    [
      text("MiniLang Compiler / Interpreter", {
        name: "slide-title",
        width: fill,
        height: hug,
        style: { fontSize: 72, bold: true, color: "#12343B", fontFace: "Aptos Display" },
      }),
      rule({ name: "rule", width: fixed(260), stroke: "#2E8B57", weight: 8 }),
      text("Lexical Analysis -> Syntax Analysis -> Semantic Analysis -> Interpretation", {
        name: "subtitle",
        width: fill,
        height: hug,
        style: { fontSize: 34, color: "#31535B", fontFace: "Aptos" },
      }),
    ],
  ),
  { frame: { left: 0, top: 0, width: 1920, height: 1080 }, baseUnit: 8 },
);

const pptxBlob = await PresentationFile.exportPptx(presentation);
await pptxBlob.save("output/test_output.pptx");
