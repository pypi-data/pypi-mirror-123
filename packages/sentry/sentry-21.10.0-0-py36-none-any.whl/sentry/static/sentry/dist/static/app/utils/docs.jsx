Object.defineProperty(exports, "__esModule", { value: true });
exports.getConfigureTracingDocsLink = exports.getDocsPlatform = void 0;
const platforms = [
    'dotnet',
    'android',
    'apple',
    'dart',
    'elixir',
    'flutter',
    'go',
    'java',
    'javascript',
    'native',
    'node',
    'perl',
    'php',
    'python',
    'react-native',
    'ruby',
    'rust',
    'unity',
];
const performancePlatforms = [
    'dotnet',
    'android',
    'apple',
    'go',
    'java',
    'javascript',
    'node',
    'php',
    'python',
    'react-native',
    'ruby',
];
function validDocPlatform(platform) {
    return platforms.includes(platform);
}
function getDocsPlatform(platform, performanceOnly) {
    // react-native is the only platform that has a dash, and supports performance so we can skip that check
    if (platform === 'react-native') {
        return 'react-native';
    }
    const index = platform.indexOf('-');
    const prefix = index >= 0 ? platform.substring(0, index) : platform;
    if (validDocPlatform(prefix)) {
        const validPerformancePrefix = performancePlatforms.includes(prefix);
        if ((performanceOnly && validPerformancePrefix) || !performanceOnly) {
            return prefix;
        }
    }
    // can't find a matching docs platform
    return null;
}
exports.getDocsPlatform = getDocsPlatform;
function getConfigureTracingDocsLink(project) {
    var _a;
    const platform = (_a = project === null || project === void 0 ? void 0 : project.platform) !== null && _a !== void 0 ? _a : null;
    const docsPlatform = platform ? getDocsPlatform(platform, true) : null;
    return docsPlatform === null
        ? null // this platform does not support performance
        : `https://docs.sentry.io/platforms/${docsPlatform}/performance/`;
}
exports.getConfigureTracingDocsLink = getConfigureTracingDocsLink;
//# sourceMappingURL=docs.jsx.map