Object.defineProperty(exports, "__esModule", { value: true });
function parseApiError(resp) {
    const { detail } = (resp && resp.responseJSON) || {};
    // return immediately if string
    if (typeof detail === 'string') {
        return detail;
    }
    if (detail && detail.message) {
        return detail.message;
    }
    return 'Unknown API Error';
}
exports.default = parseApiError;
//# sourceMappingURL=parseApiError.jsx.map