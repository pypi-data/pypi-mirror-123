Object.defineProperty(exports, "__esModule", { value: true });
const utils_1 = require("app/components/events/interfaces/debugMeta-v2/utils");
const debugImage_1 = require("app/types/debugImage");
describe('DebugMeta  - utils', () => {
    describe('getStatusWeight function', () => {
        const data = [
            {
                parameter: debugImage_1.ImageStatus.FOUND,
                result: 1,
            },
            {
                parameter: debugImage_1.ImageStatus.UNUSED,
                result: 0,
            },
            {
                parameter: null,
                result: 0,
            },
            {
                parameter: debugImage_1.ImageStatus.MISSING,
                result: 2,
            },
            {
                parameter: debugImage_1.ImageStatus.MALFORMED,
                result: 2,
            },
            {
                parameter: debugImage_1.ImageStatus.FETCHING_FAILED,
                result: 2,
            },
            {
                parameter: debugImage_1.ImageStatus.TIMEOUT,
                result: 2,
            },
            {
                parameter: debugImage_1.ImageStatus.OTHER,
                result: 2,
            },
        ];
        it('should return a number according to the passed parameter', () => {
            for (const { parameter, result } of data) {
                const statusWeight = (0, utils_1.getStatusWeight)(parameter);
                expect(statusWeight).toEqual(result);
            }
        });
    });
    describe('getFileName function', () => {
        const filePaths = [
            {
                fileName: 'libsystem_kernel.dylib',
                directory: '/usr/lib/system/',
            },
            {
                fileName: 'libsentry.dylib',
                directory: '/Users/user/Coding/sentry-native/build/',
            },
        ];
        it('should return the file name of a provided filepath', () => {
            for (const { directory, fileName } of filePaths) {
                const result = (0, utils_1.getFileName)(`${directory}${fileName}`);
                expect(result).toEqual(fileName);
            }
        });
    });
    describe('combineStatus function', () => {
        const status = [
            {
                debugStatus: debugImage_1.ImageStatus.MISSING,
                unwindStatus: debugImage_1.ImageStatus.UNUSED,
                combinedStatus: debugImage_1.ImageStatus.MISSING,
            },
            {
                debugStatus: debugImage_1.ImageStatus.FOUND,
                unwindStatus: debugImage_1.ImageStatus.MISSING,
                combinedStatus: debugImage_1.ImageStatus.MISSING,
            },
            {
                debugStatus: debugImage_1.ImageStatus.FOUND,
                unwindStatus: debugImage_1.ImageStatus.UNUSED,
                combinedStatus: debugImage_1.ImageStatus.FOUND,
            },
            {
                debugStatus: debugImage_1.ImageStatus.FOUND,
                unwindStatus: null,
                combinedStatus: debugImage_1.ImageStatus.FOUND,
            },
            {
                debugStatus: undefined,
                unwindStatus: undefined,
                combinedStatus: debugImage_1.ImageStatus.UNUSED,
            },
            {
                debugStatus: undefined,
                unwindStatus: null,
                combinedStatus: debugImage_1.ImageStatus.UNUSED,
            },
            {
                debugStatus: null,
                unwindStatus: null,
                combinedStatus: debugImage_1.ImageStatus.UNUSED,
            },
        ];
        it('should return the status according to the passed parameters', () => {
            for (const { debugStatus, unwindStatus, combinedStatus } of status) {
                const result = (0, utils_1.combineStatus)(debugStatus, unwindStatus);
                expect(result).toEqual(combinedStatus);
            }
        });
    });
});
//# sourceMappingURL=utils.spec.jsx.map