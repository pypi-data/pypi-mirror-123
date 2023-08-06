Object.defineProperty(exports, "__esModule", { value: true });
exports.fileExtensionToPlatform = exports.getFileExtension = void 0;
const FILE_EXTENSION_TO_PLATFORM = {
    jsx: 'react',
    tsx: 'react',
    js: 'javascript',
    ts: 'javascript',
    php: 'php',
    py: 'python',
    vue: 'vue',
    go: 'go',
    java: 'java',
    perl: 'perl',
    rb: 'ruby',
    rs: 'rust',
    rlib: 'rust',
    swift: 'swift',
    h: 'apple',
    m: 'apple',
    mm: 'apple',
    M: 'apple',
    ex: 'elixir',
    exs: 'elixir',
    cs: 'csharp',
    fs: 'fsharp',
    kt: 'kotlin',
    dart: 'dart',
    sc: 'scala',
    scala: 'scala',
    clj: 'clojure',
};
/**
 * Takes in path (/Users/test/sentry/something.jsx) and returns file extension (jsx)
 */
function getFileExtension(fileName) {
    // this won't work for something like .spec.jsx
    const segments = fileName.split('.');
    if (segments.length > 1) {
        return segments.pop();
    }
    return undefined;
}
exports.getFileExtension = getFileExtension;
/**
 * Takes in file extension and returns a platform string that can be passed into platformicons
 */
function fileExtensionToPlatform(fileExtension) {
    return FILE_EXTENSION_TO_PLATFORM[fileExtension];
}
exports.fileExtensionToPlatform = fileExtensionToPlatform;
//# sourceMappingURL=fileExtension.jsx.map