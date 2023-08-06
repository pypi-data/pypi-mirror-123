Object.defineProperty(exports, "__esModule", { value: true });
exports.getJavaPreamble = exports.getNativeFrame = exports.getJavaFrame = exports.getPythonFrame = exports.getPHPFrame = void 0;
const utils_1 = require("app/components/events/interfaces/frame/utils");
const utils_2 = require("app/utils");
function getJavaScriptFrame(frame) {
    let result = '';
    if ((0, utils_2.defined)(frame.function)) {
        result += '  at ' + frame.function + '(';
    }
    else {
        result += '  at ? (';
    }
    if ((0, utils_2.defined)(frame.filename)) {
        result += frame.filename;
    }
    else if ((0, utils_2.defined)(frame.module)) {
        result += frame.module;
    }
    if ((0, utils_2.defined)(frame.lineNo) && frame.lineNo >= 0) {
        result += ':' + frame.lineNo;
    }
    if ((0, utils_2.defined)(frame.colNo) && frame.colNo >= 0) {
        result += ':' + frame.colNo;
    }
    result += ')';
    return result;
}
function getRubyFrame(frame) {
    let result = '  from ';
    if ((0, utils_2.defined)(frame.filename)) {
        result += frame.filename;
    }
    else if ((0, utils_2.defined)(frame.module)) {
        result += '(' + frame.module + ')';
    }
    else {
        result += '?';
    }
    if ((0, utils_2.defined)(frame.lineNo) && frame.lineNo >= 0) {
        result += ':' + frame.lineNo;
    }
    if ((0, utils_2.defined)(frame.colNo) && frame.colNo >= 0) {
        result += ':' + frame.colNo;
    }
    if ((0, utils_2.defined)(frame.function)) {
        result += ':in `' + frame.function + "'";
    }
    return result;
}
function getPHPFrame(frame, idx) {
    const funcName = frame.function === 'null' ? '{main}' : frame.function;
    return `#${idx} ${frame.filename || frame.module}(${frame.lineNo}): ${funcName}`;
}
exports.getPHPFrame = getPHPFrame;
function getPythonFrame(frame) {
    let result = '';
    if ((0, utils_2.defined)(frame.filename)) {
        result += '  File "' + frame.filename + '"';
    }
    else if ((0, utils_2.defined)(frame.module)) {
        result += '  Module "' + frame.module + '"';
    }
    else {
        result += '  ?';
    }
    if ((0, utils_2.defined)(frame.lineNo) && frame.lineNo >= 0) {
        result += ', line ' + frame.lineNo;
    }
    if ((0, utils_2.defined)(frame.colNo) && frame.colNo >= 0) {
        result += ', col ' + frame.colNo;
    }
    if ((0, utils_2.defined)(frame.function)) {
        result += ', in ' + frame.function;
    }
    if ((0, utils_2.defined)(frame.context)) {
        frame.context.forEach(item => {
            if (item[0] === frame.lineNo) {
                result += '\n    ' + (0, utils_2.trim)(item[1]);
            }
        });
    }
    return result;
}
exports.getPythonFrame = getPythonFrame;
function getJavaFrame(frame) {
    let result = '    at';
    if ((0, utils_2.defined)(frame.module)) {
        result += ' ' + frame.module + '.';
    }
    if ((0, utils_2.defined)(frame.function)) {
        result += frame.function;
    }
    if ((0, utils_2.defined)(frame.filename)) {
        result += '(' + frame.filename;
        if ((0, utils_2.defined)(frame.lineNo) && frame.lineNo >= 0) {
            result += ':' + frame.lineNo;
        }
        result += ')';
    }
    return result;
}
exports.getJavaFrame = getJavaFrame;
function ljust(str, len) {
    return str + Array(Math.max(0, len - str.length) + 1).join(' ');
}
function getNativeFrame(frame) {
    let result = '  ';
    if ((0, utils_2.defined)(frame.package)) {
        result += ljust((0, utils_1.trimPackage)(frame.package), 20);
    }
    if ((0, utils_2.defined)(frame.instructionAddr)) {
        result += ljust(frame.instructionAddr, 12);
    }
    result += ' ' + (frame.function || frame.symbolAddr);
    if ((0, utils_2.defined)(frame.filename)) {
        result += ' (' + frame.filename;
        if ((0, utils_2.defined)(frame.lineNo) && frame.lineNo >= 0) {
            result += ':' + frame.lineNo;
        }
        result += ')';
    }
    return result;
}
exports.getNativeFrame = getNativeFrame;
function getJavaPreamble(exception) {
    let result = `${exception.type}: ${exception.value}`;
    if (exception.module) {
        result = `${exception.module}.${result}`;
    }
    return result;
}
exports.getJavaPreamble = getJavaPreamble;
function getPreamble(exception, platform) {
    switch (platform) {
        case 'java':
            return getJavaPreamble(exception);
        default:
            return exception.type + ': ' + exception.value;
    }
}
function getFrame(frame, frameIdx, platform) {
    if (frame.platform) {
        platform = frame.platform;
    }
    switch (platform) {
        case 'javascript':
            return getJavaScriptFrame(frame);
        case 'ruby':
            return getRubyFrame(frame);
        case 'php':
            return getPHPFrame(frame, frameIdx);
        case 'python':
            return getPythonFrame(frame);
        case 'java':
            return getJavaFrame(frame);
        case 'objc':
        // fallthrough
        case 'cocoa':
        // fallthrough
        case 'native':
            return getNativeFrame(frame);
        default:
            return getPythonFrame(frame);
    }
}
function render(data, platform, exception) {
    var _a;
    const frames = [];
    ((_a = data === null || data === void 0 ? void 0 : data.frames) !== null && _a !== void 0 ? _a : []).forEach((frame, frameIdx) => {
        frames.push(getFrame(frame, frameIdx, platform));
    });
    if (platform !== 'python') {
        frames.reverse();
    }
    if (exception) {
        frames.unshift(getPreamble(exception, platform));
    }
    return frames.join('\n');
}
exports.default = render;
//# sourceMappingURL=rawStacktraceContent.jsx.map