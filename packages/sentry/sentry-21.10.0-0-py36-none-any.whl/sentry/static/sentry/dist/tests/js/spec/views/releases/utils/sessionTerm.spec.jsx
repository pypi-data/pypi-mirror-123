Object.defineProperty(exports, "__esModule", { value: true });
const sessionTerm_1 = require("app/views/releases/utils/sessionTerm");
describe('Release Health Session Term', function () {
    it('dotnet terms', function () {
        // Crashes
        const crashesSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASHES, 'dotnet');
        expect(crashesSessionTerm).toEqual(sessionTerm_1.commonTermsDescription.crashes);
        // Crashed
        const crashedSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASHED, 'dotnet');
        expect(crashedSessionTerm).toEqual(sessionTerm_1.mobileTermsDescription.crashed);
        // Crash Free Users
        const crashFreeUsersSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASH_FREE_USERS, 'dotnet');
        expect(crashFreeUsersSessionTerm).toEqual(sessionTerm_1.commonTermsDescription['crash-free-users']);
        // Crash Free Sessions
        const crashFreeSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASH_FREE_SESSIONS, 'dotnet');
        expect(crashFreeSessionTerm).toEqual(sessionTerm_1.mobileTermsDescription['crash-free-sessions']);
        // Abnormal
        const abnormalSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.ABNORMAL, 'dotnet');
        expect(abnormalSessionTerm).toEqual(sessionTerm_1.mobileTermsDescription.abnormal);
        // Healthy
        const healthySessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.HEALTHY, 'dotnet');
        expect(healthySessionTerm).toEqual(sessionTerm_1.mobileTermsDescription.healthy);
        // Errored
        const erroredSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.ERRORED, 'dotnet');
        expect(erroredSessionTerm).toEqual(sessionTerm_1.mobileTermsDescription.errored);
        // Unhandled
        const unhandledSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.UNHANDLED, 'dotnet');
        expect(unhandledSessionTerm).toEqual(sessionTerm_1.mobileTermsDescription.unhandled);
    });
    it('java terms', function () {
        // Crashes
        const crashesSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASHES, 'java');
        expect(crashesSessionTerm).toEqual(sessionTerm_1.commonTermsDescription.crashes);
        // Crashed
        const crashedSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASHED, 'java');
        expect(crashedSessionTerm).toEqual(sessionTerm_1.mobileTermsDescription.crashed);
        // Crash Free Users
        const crashFreeUsersSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASH_FREE_USERS, 'java');
        expect(crashFreeUsersSessionTerm).toEqual(sessionTerm_1.commonTermsDescription['crash-free-users']);
        // Crash Free Sessions
        const crashFreeSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASH_FREE_SESSIONS, 'java');
        expect(crashFreeSessionTerm).toEqual(sessionTerm_1.mobileTermsDescription['crash-free-sessions']);
        // Abnormal
        const abnormalSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.ABNORMAL, 'java');
        expect(abnormalSessionTerm).toEqual(sessionTerm_1.mobileTermsDescription.abnormal);
        // Healthy
        const healthySessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.HEALTHY, 'java');
        expect(healthySessionTerm).toEqual(sessionTerm_1.mobileTermsDescription.healthy);
        // Errored
        const erroredSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.ERRORED, 'java');
        expect(erroredSessionTerm).toEqual(sessionTerm_1.mobileTermsDescription.errored);
        // Unhandled
        const unhandledSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.UNHANDLED, 'java');
        expect(unhandledSessionTerm).toEqual(sessionTerm_1.mobileTermsDescription.unhandled);
    });
    it('java-spring terms', function () {
        // Crashes
        const crashesSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASHES, 'java-spring');
        expect(crashesSessionTerm).toEqual('A request that resulted in an unhandled exception and hence a Server Error response');
        // Crashed
        const crashedSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASHED, 'java-spring');
        expect(crashedSessionTerm).toEqual(sessionTerm_1.mobileTermsDescription.crashed);
        // Crash Free Users
        const crashFreeUsersSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASH_FREE_USERS, 'java-spring');
        expect(crashFreeUsersSessionTerm).toEqual(sessionTerm_1.commonTermsDescription['crash-free-users']);
        // Crash Free Sessions
        const crashFreeSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASH_FREE_SESSIONS, 'java-spring');
        expect(crashFreeSessionTerm).toEqual(sessionTerm_1.mobileTermsDescription['crash-free-sessions']);
        // Abnormal
        const abnormalSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.ABNORMAL, 'java-spring');
        expect(abnormalSessionTerm).toEqual(sessionTerm_1.mobileTermsDescription.abnormal);
        // Healthy
        const healthySessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.HEALTHY, 'java-spring');
        expect(healthySessionTerm).toEqual(sessionTerm_1.mobileTermsDescription.healthy);
        // Errored
        const erroredSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.ERRORED, 'java-spring');
        expect(erroredSessionTerm).toEqual(sessionTerm_1.mobileTermsDescription.errored);
        // Unhandled
        const unhandledSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.UNHANDLED, 'java-spring');
        expect(unhandledSessionTerm).toEqual(sessionTerm_1.mobileTermsDescription.unhandled);
    });
    it('dotnet-aspnetcore terms', function () {
        // Crashes
        const crashesSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASHES, 'dotnet-aspnetcore');
        expect(crashesSessionTerm).toEqual('A request that resulted in an unhandled exception and hence a Server Error response');
        // Crashed
        const crashedSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASHED, 'dotnet-aspnetcore');
        expect(crashedSessionTerm).toEqual(sessionTerm_1.mobileTermsDescription.crashed);
        // Crash Free Users
        const crashFreeUsersSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASH_FREE_USERS, 'dotnet-aspnetcore');
        expect(crashFreeUsersSessionTerm).toEqual(sessionTerm_1.commonTermsDescription['crash-free-users']);
        // Crash Free Sessions
        const crashFreeSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASH_FREE_SESSIONS, 'dotnet-aspnetcore');
        expect(crashFreeSessionTerm).toEqual(sessionTerm_1.mobileTermsDescription['crash-free-sessions']);
        // Abnormal
        const abnormalSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.ABNORMAL, 'dotnet-aspnetcore');
        expect(abnormalSessionTerm).toEqual(sessionTerm_1.mobileTermsDescription.abnormal);
        // Healthy
        const healthySessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.HEALTHY, 'dotnet-aspnetcore');
        expect(healthySessionTerm).toEqual(sessionTerm_1.mobileTermsDescription.healthy);
        // Errored
        const erroredSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.ERRORED, 'dotnet-aspnetcore');
        expect(erroredSessionTerm).toEqual(sessionTerm_1.mobileTermsDescription.errored);
        // Unhandled
        const unhandledSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.UNHANDLED, 'dotnet-aspnetcore');
        expect(unhandledSessionTerm).toEqual(sessionTerm_1.mobileTermsDescription.unhandled);
    });
    it('android terms', function () {
        // Crashes
        const crashesSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASHES, 'android');
        expect(crashesSessionTerm).toEqual(sessionTerm_1.commonTermsDescription.crashes);
        // Crashed
        const crashedSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASHED, 'android');
        expect(crashedSessionTerm).toEqual('An unhandled exception that resulted in the application crashing');
        // Crash Free Users
        const crashFreeUsersSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASH_FREE_USERS, 'android');
        expect(crashFreeUsersSessionTerm).toEqual(sessionTerm_1.commonTermsDescription['crash-free-users']);
        // Crash Free Sessions
        const crashFreeSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASH_FREE_SESSIONS, 'android');
        expect(crashFreeSessionTerm).toEqual(sessionTerm_1.mobileTermsDescription['crash-free-sessions']);
        // Abnormal
        const abnormalSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.ABNORMAL, 'android');
        expect(abnormalSessionTerm).toEqual(sessionTerm_1.mobileTermsDescription.abnormal);
        // Healthy
        const healthySessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.HEALTHY, 'android');
        expect(healthySessionTerm).toEqual(sessionTerm_1.mobileTermsDescription.healthy);
        // Errored
        const erroredSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.ERRORED, 'android');
        expect(erroredSessionTerm).toEqual(sessionTerm_1.mobileTermsDescription.errored);
        // Unhandled
        const unhandledSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.UNHANDLED, 'android');
        expect(unhandledSessionTerm).toEqual(sessionTerm_1.mobileTermsDescription.unhandled);
    });
    it('cordova terms', function () {
        // Crashes
        const crashesSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASHES, 'cordova');
        expect(crashesSessionTerm).toEqual(sessionTerm_1.commonTermsDescription.crashes);
        // Crashed
        const crashedSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASHED, 'cordova');
        expect(crashedSessionTerm).toEqual('An unhandled exception that resulted in the application crashing');
        // Crash Free Users
        const crashFreeUsersSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASH_FREE_USERS, 'cordova');
        expect(crashFreeUsersSessionTerm).toEqual(sessionTerm_1.commonTermsDescription['crash-free-users']);
        // Crash Free Sessions
        const crashFreeSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASH_FREE_SESSIONS, 'cordova');
        expect(crashFreeSessionTerm).toEqual(sessionTerm_1.mobileTermsDescription['crash-free-sessions']);
        // Abnormal
        const abnormalSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.ABNORMAL, 'cordova');
        expect(abnormalSessionTerm).toEqual(sessionTerm_1.mobileTermsDescription.abnormal);
        // Healthy
        const healthySessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.HEALTHY, 'cordova');
        expect(healthySessionTerm).toEqual(sessionTerm_1.mobileTermsDescription.healthy);
        // Errored
        const erroredSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.ERRORED, 'cordova');
        expect(erroredSessionTerm).toEqual(sessionTerm_1.mobileTermsDescription.errored);
        // Unhandled
        const unhandledSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.UNHANDLED, 'cordova');
        expect(unhandledSessionTerm).toEqual(sessionTerm_1.mobileTermsDescription.unhandled);
    });
    it('react-native terms', function () {
        // Crashes
        const crashesSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASHES, 'react-native');
        expect(crashesSessionTerm).toEqual(sessionTerm_1.commonTermsDescription.crashes);
        // Crashed
        const crashedSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASHED, 'react-native');
        expect(crashedSessionTerm).toEqual('An unhandled exception that resulted in the application crashing');
        // Crash Free Users
        const crashFreeUsersSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASH_FREE_USERS, 'react-native');
        expect(crashFreeUsersSessionTerm).toEqual(sessionTerm_1.commonTermsDescription['crash-free-users']);
        // Crash Free Sessions
        const crashFreeSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASH_FREE_SESSIONS, 'react-native');
        expect(crashFreeSessionTerm).toEqual(sessionTerm_1.mobileTermsDescription['crash-free-sessions']);
        // Abnormal
        const abnormalSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.ABNORMAL, 'react-native');
        expect(abnormalSessionTerm).toEqual(sessionTerm_1.mobileTermsDescription.abnormal);
        // Healthy
        const healthySessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.HEALTHY, 'react-native');
        expect(healthySessionTerm).toEqual(sessionTerm_1.mobileTermsDescription.healthy);
        // Errored
        const erroredSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.ERRORED, 'react-native');
        expect(erroredSessionTerm).toEqual(sessionTerm_1.mobileTermsDescription.errored);
        // Unhandled
        const unhandledSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.UNHANDLED, 'react-native');
        expect(unhandledSessionTerm).toEqual(sessionTerm_1.mobileTermsDescription.unhandled);
    });
    it('flutter terms', function () {
        // Crashes
        const crashesSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASHES, 'flutter');
        expect(crashesSessionTerm).toEqual(sessionTerm_1.commonTermsDescription.crashes);
        // Crashed
        const crashedSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASHED, 'flutter');
        expect(crashedSessionTerm).toEqual('An unhandled exception that resulted in the application crashing');
        // Crash Free Users
        const crashFreeUsersSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASH_FREE_USERS, 'flutter');
        expect(crashFreeUsersSessionTerm).toEqual(sessionTerm_1.commonTermsDescription['crash-free-users']);
        // Crash Free Sessions
        const crashFreeSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASH_FREE_SESSIONS, 'flutter');
        expect(crashFreeSessionTerm).toEqual(sessionTerm_1.mobileTermsDescription['crash-free-sessions']);
        // Abnormal
        const abnormalSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.ABNORMAL, 'flutter');
        expect(abnormalSessionTerm).toEqual(sessionTerm_1.mobileTermsDescription.abnormal);
        // Healthy
        const healthySessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.HEALTHY, 'flutter');
        expect(healthySessionTerm).toEqual(sessionTerm_1.mobileTermsDescription.healthy);
        // Errored
        const erroredSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.ERRORED, 'flutter');
        expect(erroredSessionTerm).toEqual(sessionTerm_1.mobileTermsDescription.errored);
        // Unhandled
        const unhandledSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.UNHANDLED, 'flutter');
        expect(unhandledSessionTerm).toEqual(sessionTerm_1.mobileTermsDescription.unhandled);
    });
    it('apple terms', function () {
        // Crashes
        const crashesSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASHES, 'apple-macos');
        expect(crashesSessionTerm).toEqual(sessionTerm_1.commonTermsDescription.crashes);
        // Crashed
        const crashedSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASHED, 'apple-macos');
        expect(crashedSessionTerm).toEqual('An error that resulted in the application crashing');
        // Crash Free Users
        const crashFreeUsersSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASH_FREE_USERS, 'apple-macos');
        expect(crashFreeUsersSessionTerm).toEqual(sessionTerm_1.commonTermsDescription['crash-free-users']);
        // Crash Free Sessions
        const crashFreeSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASH_FREE_SESSIONS, 'apple-macos');
        expect(crashFreeSessionTerm).toEqual(sessionTerm_1.mobileTermsDescription['crash-free-sessions']);
        // Abnormal
        const abnormalSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.ABNORMAL, 'apple-macos');
        expect(abnormalSessionTerm).toEqual(sessionTerm_1.mobileTermsDescription.abnormal);
        // Healthy
        const healthySessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.HEALTHY, 'apple-macos');
        expect(healthySessionTerm).toEqual(sessionTerm_1.mobileTermsDescription.healthy);
        // Errored
        const erroredSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.ERRORED, 'apple-macos');
        expect(erroredSessionTerm).toEqual(sessionTerm_1.mobileTermsDescription.errored);
        // Unhandled
        const unhandledSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.UNHANDLED, 'apple-macos');
        expect(unhandledSessionTerm).toEqual(sessionTerm_1.mobileTermsDescription.unhandled);
    });
    it('node-express terms', function () {
        // Crashes
        const crashesSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASHES, 'node-express');
        expect(crashesSessionTerm).toEqual(sessionTerm_1.commonTermsDescription.crashes);
        // Crashed
        const crashedSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASHED, 'node-express');
        expect(crashedSessionTerm).toEqual('During the session an unhandled global error/promise rejection occurred.');
        // Crash Free Users
        const crashFreeUsersSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASH_FREE_USERS, 'node-express');
        expect(crashFreeUsersSessionTerm).toEqual(sessionTerm_1.commonTermsDescription['crash-free-users']);
        // Crash Free Sessions
        const crashFreeSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASH_FREE_SESSIONS, 'node-express');
        expect(crashFreeSessionTerm).toEqual(sessionTerm_1.commonTermsDescription['crash-free-sessions']);
        // Abnormal
        const abnormalSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.ABNORMAL, 'node-express');
        expect(abnormalSessionTerm).toEqual('Non applicable for Javascript.');
        // Healthy
        const healthySessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.HEALTHY, 'node-express');
        expect(healthySessionTerm).toEqual('No errors were captured during session life-time.');
        // Errored
        const erroredSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.ERRORED, 'node-express');
        expect(erroredSessionTerm).toEqual('During the session at least one handled error occurred.');
        // Unhandled
        const unhandledSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.UNHANDLED, 'node-express');
        expect(unhandledSessionTerm).toEqual("An error was captured by the global 'onerror' or 'onunhandledrejection' handler.");
    });
    it('javascript terms', function () {
        // Crashes
        const crashesSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASHES, 'javascript');
        expect(crashesSessionTerm).toEqual(sessionTerm_1.commonTermsDescription.crashes);
        // Crashed
        const crashedSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASHED, 'javascript');
        expect(crashedSessionTerm).toEqual('During the session an unhandled global error/promise rejection occurred.');
        // Crash Free Users
        const crashFreeUsersSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASH_FREE_USERS, 'javascript');
        expect(crashFreeUsersSessionTerm).toEqual(sessionTerm_1.commonTermsDescription['crash-free-users']);
        // Crash Free Sessions
        const crashFreeSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASH_FREE_SESSIONS, 'javascript');
        expect(crashFreeSessionTerm).toEqual(sessionTerm_1.commonTermsDescription['crash-free-sessions']);
        // Abnormal
        const abnormalSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.ABNORMAL, 'javascript');
        expect(abnormalSessionTerm).toEqual('Non applicable for Javascript.');
        // Healthy
        const healthySessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.HEALTHY, 'javascript');
        expect(healthySessionTerm).toEqual('No errors were captured during session life-time.');
        // Errored
        const erroredSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.ERRORED, 'javascript');
        expect(erroredSessionTerm).toEqual('During the session at least one handled error occurred.');
        // Unhandled
        const unhandledSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.UNHANDLED, 'javascript');
        expect(unhandledSessionTerm).toEqual("An error was captured by the global 'onerror' or 'onunhandledrejection' handler.");
    });
    it('rust terms', function () {
        // Crashes
        const crashesSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASHES, 'rust');
        expect(crashesSessionTerm).toEqual(sessionTerm_1.commonTermsDescription.crashes);
        // Crashed
        const crashedSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASHED, 'rust');
        expect(crashedSessionTerm).toEqual('The application had an unrecoverable error (a panic)');
        // Crash Free Users
        const crashFreeUsersSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASH_FREE_USERS, 'rust');
        expect(crashFreeUsersSessionTerm).toEqual(sessionTerm_1.commonTermsDescription['crash-free-users']);
        // Crash Free Sessions
        const crashFreeSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASH_FREE_SESSIONS, 'rust');
        expect(crashFreeSessionTerm).toEqual(sessionTerm_1.commonTermsDescription['crash-free-sessions']);
        // Abnormal
        const abnormalSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.ABNORMAL, 'rust');
        expect(abnormalSessionTerm).toEqual(sessionTerm_1.desktopTermDescriptions.abnormal);
        // Healthy
        const healthySessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.HEALTHY, 'rust');
        expect(healthySessionTerm).toEqual(sessionTerm_1.desktopTermDescriptions.healthy);
        // Errored
        const erroredSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.ERRORED, 'rust');
        expect(erroredSessionTerm).toEqual(sessionTerm_1.desktopTermDescriptions.errored);
        // Unhandled
        const unhandledSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.UNHANDLED, 'rust');
        expect(unhandledSessionTerm).toEqual(sessionTerm_1.desktopTermDescriptions.unhandled);
    });
    it('apple-ios terms', function () {
        // Crashes
        const crashesSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASHES, 'apple-ios');
        expect(crashesSessionTerm).toEqual(sessionTerm_1.commonTermsDescription.crashes);
        // Crashed
        const crashedSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASHED, 'apple-ios');
        expect(crashedSessionTerm).toEqual(sessionTerm_1.desktopTermDescriptions.crashed);
        // Crash Free Users
        const crashFreeUsersSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASH_FREE_USERS, 'apple-ios');
        expect(crashFreeUsersSessionTerm).toEqual(sessionTerm_1.commonTermsDescription['crash-free-users']);
        // Crash Free Sessions
        const crashFreeSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASH_FREE_SESSIONS, 'apple-ios');
        expect(crashFreeSessionTerm).toEqual(sessionTerm_1.commonTermsDescription['crash-free-sessions']);
        // Abnormal
        const abnormalSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.ABNORMAL, 'apple-ios');
        expect(abnormalSessionTerm).toEqual(sessionTerm_1.desktopTermDescriptions.abnormal);
        // Healthy
        const healthySessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.HEALTHY, 'apple-ios');
        expect(healthySessionTerm).toEqual(sessionTerm_1.desktopTermDescriptions.healthy);
        // Errored
        const erroredSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.ERRORED, 'apple-ios');
        expect(erroredSessionTerm).toEqual(sessionTerm_1.desktopTermDescriptions.errored);
        // Unhandled
        const unhandledSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.UNHANDLED, 'apple-ios');
        expect(unhandledSessionTerm).toEqual(sessionTerm_1.desktopTermDescriptions.unhandled);
    });
    it('minidump terms', function () {
        // Crashes
        const crashesSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASHES, 'minidump');
        expect(crashesSessionTerm).toEqual(sessionTerm_1.commonTermsDescription.crashes);
        // Crashed
        const crashedSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASHED, 'minidump');
        expect(crashedSessionTerm).toEqual(sessionTerm_1.desktopTermDescriptions.crashed);
        // Crash Free Users
        const crashFreeUsersSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASH_FREE_USERS, 'minidump');
        expect(crashFreeUsersSessionTerm).toEqual(sessionTerm_1.commonTermsDescription['crash-free-users']);
        // Crash Free Sessions
        const crashFreeSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASH_FREE_SESSIONS, 'minidump');
        expect(crashFreeSessionTerm).toEqual(sessionTerm_1.commonTermsDescription['crash-free-sessions']);
        // Abnormal
        const abnormalSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.ABNORMAL, 'minidump');
        expect(abnormalSessionTerm).toEqual(sessionTerm_1.desktopTermDescriptions.abnormal);
        // Healthy
        const healthySessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.HEALTHY, 'minidump');
        expect(healthySessionTerm).toEqual(sessionTerm_1.desktopTermDescriptions.healthy);
        // Errored
        const erroredSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.ERRORED, 'minidump');
        expect(erroredSessionTerm).toEqual(sessionTerm_1.desktopTermDescriptions.errored);
        // Unhandled
        const unhandledSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.UNHANDLED, 'minidump');
        expect(unhandledSessionTerm).toEqual(sessionTerm_1.desktopTermDescriptions.unhandled);
    });
    it('native terms', function () {
        // Crashes
        const crashesSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASHES, 'native');
        expect(crashesSessionTerm).toEqual(sessionTerm_1.commonTermsDescription.crashes);
        // Crashed
        const crashedSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASHED, 'native');
        expect(crashedSessionTerm).toEqual(sessionTerm_1.desktopTermDescriptions.crashed);
        // Crash Free Users
        const crashFreeUsersSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASH_FREE_USERS, 'native');
        expect(crashFreeUsersSessionTerm).toEqual(sessionTerm_1.commonTermsDescription['crash-free-users']);
        // Crash Free Sessions
        const crashFreeSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASH_FREE_SESSIONS, 'native');
        expect(crashFreeSessionTerm).toEqual(sessionTerm_1.commonTermsDescription['crash-free-sessions']);
        // Abnormal
        const abnormalSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.ABNORMAL, 'native');
        expect(abnormalSessionTerm).toEqual(sessionTerm_1.desktopTermDescriptions.abnormal);
        // Healthy
        const healthySessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.HEALTHY, 'native');
        expect(healthySessionTerm).toEqual(sessionTerm_1.desktopTermDescriptions.healthy);
        // Errored
        const erroredSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.ERRORED, 'native');
        expect(erroredSessionTerm).toEqual(sessionTerm_1.desktopTermDescriptions.errored);
        // Unhandled
        const unhandledSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.UNHANDLED, 'native');
        expect(unhandledSessionTerm).toEqual(sessionTerm_1.desktopTermDescriptions.unhandled);
    });
    it('python terms', function () {
        // Crashes
        const crashesSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASHES, 'python');
        expect(crashesSessionTerm).toEqual(sessionTerm_1.commonTermsDescription.crashes);
        // Crashed
        const crashedSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASHED, 'python');
        expect(crashedSessionTerm).toEqual('Number of users who experienced an unhandled error');
        // Crash Free Users
        const crashFreeUsersSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASH_FREE_USERS, 'python');
        expect(crashFreeUsersSessionTerm).toEqual(sessionTerm_1.commonTermsDescription['crash-free-users']);
        // Crash Free Sessions
        const crashFreeSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASH_FREE_SESSIONS, 'python');
        expect(crashFreeSessionTerm).toEqual(sessionTerm_1.commonTermsDescription['crash-free-sessions']);
        // Abnormal
        const abnormalSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.ABNORMAL, 'python');
        expect(abnormalSessionTerm).toEqual('An unknown session exit');
        // Healthy
        const healthySessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.HEALTHY, 'python');
        expect(healthySessionTerm).toEqual(sessionTerm_1.mobileTermsDescription.healthy);
        // Errored
        const erroredSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.ERRORED, 'python');
        expect(erroredSessionTerm).toEqual(sessionTerm_1.mobileTermsDescription.errored);
        // Unhandled
        const unhandledSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.UNHANDLED, 'python');
        expect(unhandledSessionTerm).toEqual(sessionTerm_1.mobileTermsDescription.unhandled);
    });
    it('default terms', function () {
        // Crashes
        const crashesSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASHES, null);
        expect(crashesSessionTerm).toEqual(sessionTerm_1.commonTermsDescription.crashes);
        // Crashed
        const crashedSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASHED, null);
        expect(crashedSessionTerm).toEqual('Number of users who experienced an unhandled error');
        // Crash Free Users
        const crashFreeUsersSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASH_FREE_USERS, null);
        expect(crashFreeUsersSessionTerm).toEqual(sessionTerm_1.commonTermsDescription['crash-free-users']);
        // Crash Free Sessions
        const crashFreeSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASH_FREE_SESSIONS, null);
        expect(crashFreeSessionTerm).toEqual(sessionTerm_1.commonTermsDescription['crash-free-sessions']);
        // Abnormal
        const abnormalSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.ABNORMAL, null);
        expect(abnormalSessionTerm).toEqual('An unknown session exit');
        // Healthy
        const healthySessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.HEALTHY, null);
        expect(healthySessionTerm).toEqual(sessionTerm_1.mobileTermsDescription.healthy);
        // Errored
        const erroredSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.ERRORED, null);
        expect(erroredSessionTerm).toEqual(sessionTerm_1.mobileTermsDescription.errored);
        // Unhandled
        const unhandledSessionTerm = (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.UNHANDLED, null);
        expect(unhandledSessionTerm).toEqual(sessionTerm_1.mobileTermsDescription.unhandled);
    });
});
//# sourceMappingURL=sessionTerm.spec.jsx.map