Object.defineProperty(exports, "__esModule", { value: true });
exports.selectText = void 0;
function selectText(node) {
    if (node instanceof HTMLInputElement && node.type === 'text') {
        node.select();
    }
    else if (node instanceof Node && window.getSelection) {
        const range = document.createRange();
        range.selectNode(node);
        const selection = window.getSelection();
        if (selection) {
            selection.removeAllRanges();
            selection.addRange(range);
        }
    }
}
exports.selectText = selectText;
//# sourceMappingURL=selectText.jsx.map