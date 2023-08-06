Object.defineProperty(exports, "__esModule", { value: true });
exports.isExpandable = exports.hasAssembly = exports.hasContextRegisters = exports.hasContextVars = exports.hasContextSource = exports.isDotnet = exports.getFrameHint = exports.getPlatform = exports.trimPackage = void 0;
const types_1 = require("app/components/events/interfaces/types");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const utils_1 = require("app/utils");
function trimPackage(pkg) {
    const pieces = pkg.split(/^([a-z]:\\|\\\\)/i.test(pkg) ? '\\' : '/');
    const filename = pieces[pieces.length - 1] || pieces[pieces.length - 2] || pkg;
    return filename.replace(/\.(dylib|so|a|dll|exe)$/, '');
}
exports.trimPackage = trimPackage;
function getPlatform(dataPlatform, platform) {
    // prioritize the frame platform but fall back to the platform
    // of the stack trace / exception
    return dataPlatform || platform;
}
exports.getPlatform = getPlatform;
function getFrameHint(frame) {
    // returning [hintText, hintIcon]
    const { symbolicatorStatus } = frame;
    const func = frame.function || '<unknown>';
    // Custom color used to match adjacent text.
    const warningIcon = <icons_1.IconQuestion size="xs" color={'#2c45a8'}/>;
    const errorIcon = <icons_1.IconWarning size="xs" color="red300"/>;
    if (func.match(/^@objc\s/)) {
        return [(0, locale_1.t)('Objective-C -> Swift shim frame'), warningIcon];
    }
    if (func.match(/^__?hidden#\d+/)) {
        return [(0, locale_1.t)('Hidden function from bitcode build'), errorIcon];
    }
    if (!symbolicatorStatus && func === '<unknown>') {
        // Only render this if the event was not symbolicated.
        return [(0, locale_1.t)('No function name was supplied by the client SDK.'), warningIcon];
    }
    if (func === '<unknown>' ||
        (func === '<redacted>' && symbolicatorStatus === types_1.SymbolicatorStatus.MISSING_SYMBOL)) {
        switch (symbolicatorStatus) {
            case types_1.SymbolicatorStatus.MISSING_SYMBOL:
                return [(0, locale_1.t)('The symbol was not found within the debug file.'), warningIcon];
            case types_1.SymbolicatorStatus.UNKNOWN_IMAGE:
                return [(0, locale_1.t)('No image is specified for the address of the frame.'), warningIcon];
            case types_1.SymbolicatorStatus.MISSING:
                return [
                    (0, locale_1.t)('The debug file could not be retrieved from any of the sources.'),
                    errorIcon,
                ];
            case types_1.SymbolicatorStatus.MALFORMED:
                return [(0, locale_1.t)('The retrieved debug file could not be processed.'), errorIcon];
            default:
        }
    }
    if (func === '<redacted>') {
        return [(0, locale_1.t)('Unknown system frame. Usually from beta SDKs'), warningIcon];
    }
    return [null, null];
}
exports.getFrameHint = getFrameHint;
function isDotnet(platform) {
    // csharp platform represents .NET and can be F#, VB or any language targeting CLS (the Common Language Specification)
    return platform === 'csharp';
}
exports.isDotnet = isDotnet;
function hasContextSource(frame) {
    return (0, utils_1.defined)(frame.context) && !!frame.context.length;
}
exports.hasContextSource = hasContextSource;
function hasContextVars(frame) {
    return !(0, utils_1.objectIsEmpty)(frame.vars || {});
}
exports.hasContextVars = hasContextVars;
function hasContextRegisters(registers) {
    return !(0, utils_1.objectIsEmpty)(registers);
}
exports.hasContextRegisters = hasContextRegisters;
function hasAssembly(frame, platform) {
    return (isDotnet(getPlatform(frame.platform, platform !== null && platform !== void 0 ? platform : 'other')) && (0, utils_1.defined)(frame.package));
}
exports.hasAssembly = hasAssembly;
function isExpandable({ frame, registers, emptySourceNotation, platform, isOnlyFrame, }) {
    return ((!isOnlyFrame && emptySourceNotation) ||
        hasContextSource(frame) ||
        hasContextVars(frame) ||
        hasContextRegisters(registers) ||
        hasAssembly(frame, platform));
}
exports.isExpandable = isExpandable;
//# sourceMappingURL=utils.jsx.map