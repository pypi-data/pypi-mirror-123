Object.defineProperty(exports, "__esModule", { value: true });
exports.getSessionTermDescription = exports.desktopTermDescriptions = exports.mobileTermsDescription = exports.commonTermsDescription = exports.sessionTerm = exports.SessionTerm = void 0;
const locale_1 = require("app/locale");
var SessionTerm;
(function (SessionTerm) {
    SessionTerm["CRASHES"] = "crashes";
    SessionTerm["CRASHED"] = "crashed";
    SessionTerm["ABNORMAL"] = "abnormal";
    SessionTerm["CRASH_FREE"] = "crashFree";
    SessionTerm["CRASH_FREE_USERS"] = "crash-free-users";
    SessionTerm["CRASH_FREE_SESSIONS"] = "crash-free-sessions";
    SessionTerm["HEALTHY"] = "healthy";
    SessionTerm["ERRORED"] = "errored";
    SessionTerm["UNHANDLED"] = "unhandled";
    SessionTerm["STABILITY"] = "stability";
    SessionTerm["ADOPTION"] = "adoption";
})(SessionTerm = exports.SessionTerm || (exports.SessionTerm = {}));
exports.sessionTerm = {
    [SessionTerm.CRASHES]: (0, locale_1.t)('Crashes'),
    [SessionTerm.CRASHED]: (0, locale_1.t)('Crashed'),
    [SessionTerm.ABNORMAL]: (0, locale_1.t)('Abnormal'),
    [SessionTerm.CRASH_FREE_USERS]: (0, locale_1.t)('Crash Free Users'),
    [SessionTerm.CRASH_FREE_SESSIONS]: (0, locale_1.t)('Crash Free Sessions'),
    [SessionTerm.HEALTHY]: (0, locale_1.t)('Healthy'),
    [SessionTerm.ERRORED]: (0, locale_1.t)('Errored'),
    [SessionTerm.UNHANDLED]: (0, locale_1.t)('Unhandled'),
    [SessionTerm.ADOPTION]: (0, locale_1.t)('Adoption'),
    duration: (0, locale_1.t)('Session Duration'),
    otherCrashed: (0, locale_1.t)('Other Crashed'),
    otherAbnormal: (0, locale_1.t)('Other Abnormal'),
    otherErrored: (0, locale_1.t)('Other Errored'),
    otherHealthy: (0, locale_1.t)('Other Healthy'),
    otherCrashFreeUsers: (0, locale_1.t)('Other Crash Free Users'),
    otherCrashFreeSessions: (0, locale_1.t)('Other Crash Free Sessions'),
    otherReleases: (0, locale_1.t)('Other Releases'),
};
// This should never be used directly (except in tests)
exports.commonTermsDescription = {
    [SessionTerm.CRASHES]: (0, locale_1.t)('Number of sessions with a crashed state'),
    [SessionTerm.CRASH_FREE]: (0, locale_1.t)('Percentage of sessions/users who did not experience a crash.'),
    [SessionTerm.CRASH_FREE_USERS]: (0, locale_1.t)('Percentage of unique users with non-crashed sessions'),
    [SessionTerm.CRASH_FREE_SESSIONS]: (0, locale_1.t)('Percentage of non-crashed sessions'),
    [SessionTerm.STABILITY]: (0, locale_1.t)('The percentage of crash free sessions.'),
    [SessionTerm.ADOPTION]: (0, locale_1.t)('Adoption compares the sessions or users of a release with the total sessions or users for this project in the last 24 hours.'),
};
// This should never be used directly (except in tests)
exports.mobileTermsDescription = {
    [SessionTerm.CRASHED]: (0, locale_1.t)('The process was terminated due to an unhandled exception or a request to the server that ended with an error'),
    [SessionTerm.CRASH_FREE_SESSIONS]: (0, locale_1.t)('Percentage of non-crashed sessions'),
    [SessionTerm.ABNORMAL]: (0, locale_1.t)('An unknown session exit. Like due to loss of power or killed by the operating system'),
    [SessionTerm.HEALTHY]: (0, locale_1.t)('A session without errors'),
    [SessionTerm.ERRORED]: (0, locale_1.t)('A session with errors'),
    [SessionTerm.UNHANDLED]: (0, locale_1.t)('Not handled by user code'),
};
// This should never be used directly (except in tests)
exports.desktopTermDescriptions = {
    crashed: (0, locale_1.t)('The application crashed with a hard crash (eg. segfault)'),
    [SessionTerm.ABNORMAL]: (0, locale_1.t)('The application did not properly end the session, for example, due to force-quit'),
    [SessionTerm.HEALTHY]: (0, locale_1.t)('The application exited normally and did not observe any errors'),
    [SessionTerm.ERRORED]: (0, locale_1.t)('The application exited normally but observed error events while running'),
    [SessionTerm.UNHANDLED]: (0, locale_1.t)('The application crashed with a hard crash'),
};
function getTermDescriptions(platform) {
    const technology = platform === 'react-native' ||
        platform === 'java-spring' ||
        platform === 'apple-ios' ||
        platform === 'dotnet-aspnetcore'
        ? platform
        : platform === null || platform === void 0 ? void 0 : platform.split('-')[0];
    switch (technology) {
        case 'dotnet':
        case 'java':
            return Object.assign(Object.assign({}, exports.commonTermsDescription), exports.mobileTermsDescription);
        case 'java-spring':
        case 'dotnet-aspnetcore':
            return Object.assign(Object.assign(Object.assign({}, exports.commonTermsDescription), exports.mobileTermsDescription), { [SessionTerm.CRASHES]: (0, locale_1.t)('A request that resulted in an unhandled exception and hence a Server Error response') });
        case 'android':
        case 'cordova':
        case 'react-native':
        case 'flutter':
            return Object.assign(Object.assign(Object.assign({}, exports.commonTermsDescription), exports.mobileTermsDescription), { [SessionTerm.CRASHED]: (0, locale_1.t)('An unhandled exception that resulted in the application crashing') });
        case 'apple': {
            return Object.assign(Object.assign(Object.assign({}, exports.commonTermsDescription), exports.mobileTermsDescription), { [SessionTerm.CRASHED]: (0, locale_1.t)('An error that resulted in the application crashing') });
        }
        case 'node':
        case 'javascript':
            return Object.assign(Object.assign({}, exports.commonTermsDescription), { [SessionTerm.CRASHED]: (0, locale_1.t)('During the session an unhandled global error/promise rejection occurred.'), [SessionTerm.ABNORMAL]: (0, locale_1.t)('Non applicable for Javascript.'), [SessionTerm.HEALTHY]: (0, locale_1.t)('No errors were captured during session life-time.'), [SessionTerm.ERRORED]: (0, locale_1.t)('During the session at least one handled error occurred.'), [SessionTerm.UNHANDLED]: "An error was captured by the global 'onerror' or 'onunhandledrejection' handler." });
        case 'apple-ios':
        case 'minidump':
        case 'native':
            return Object.assign(Object.assign({}, exports.commonTermsDescription), exports.desktopTermDescriptions);
        case 'rust':
            return Object.assign(Object.assign(Object.assign({}, exports.commonTermsDescription), exports.desktopTermDescriptions), { [SessionTerm.CRASHED]: (0, locale_1.t)('The application had an unrecoverable error (a panic)') });
        default:
            return Object.assign(Object.assign({}, exports.commonTermsDescription), { [SessionTerm.CRASHED]: (0, locale_1.t)('Number of users who experienced an unhandled error'), [SessionTerm.ABNORMAL]: (0, locale_1.t)('An unknown session exit'), [SessionTerm.HEALTHY]: exports.mobileTermsDescription.healthy, [SessionTerm.ERRORED]: exports.mobileTermsDescription.errored, [SessionTerm.UNHANDLED]: exports.mobileTermsDescription.unhandled });
    }
}
function getSessionTermDescription(term, platform) {
    return getTermDescriptions(platform)[term];
}
exports.getSessionTermDescription = getSessionTermDescription;
//# sourceMappingURL=sessionTerm.jsx.map