Object.defineProperty(exports, "__esModule", { value: true });
exports.isNotSharedOrganization = exports.assertType = exports.assert = void 0;
// from:
// - https://www.typescriptlang.org/docs/handbook/release-notes/typescript-3-7.html#assertion-functions
// - https://www.typescriptlang.org/play/#example/assertion-functions
// This declares a function which asserts that the expression called
// value is true:
// eslint-disable-next-line prettier/prettier
function assert(_value) { }
exports.assert = assert;
// This declares a function which asserts that the expression called
// value is of type Type:
// eslint-disable-next-line prettier/prettier
function assertType(_value) { }
exports.assertType = assertType;
function isNotSharedOrganization(maybe) {
    return typeof maybe.id !== 'undefined';
}
exports.isNotSharedOrganization = isNotSharedOrganization;
//# sourceMappingURL=utils.jsx.map