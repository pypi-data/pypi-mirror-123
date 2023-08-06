Object.defineProperty(exports, "__esModule", { value: true });
exports.domId = void 0;
function domId(prefix) {
    return prefix + Math.random().toString(36).substr(2, 10);
}
exports.domId = domId;
//# sourceMappingURL=domId.jsx.map