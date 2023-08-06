Object.defineProperty(exports, "__esModule", { value: true });
exports.findAllByTextContent = exports.findByTextContent = void 0;
// Taken from https://stackoverflow.com/a/56859650/1015027
function findTextWithMarkup(contentNode, textMatch) {
    const hasText = (node) => node.textContent === textMatch;
    const nodeHasText = hasText(contentNode);
    const childrenDontHaveText = Array.from((contentNode === null || contentNode === void 0 ? void 0 : contentNode.children) || []).every(child => !hasText(child));
    return nodeHasText && childrenDontHaveText;
}
/**
 * Search for a text broken up by multiple html elements
 * e.g.: <div>Hello <span>world</span></div>
 */
function findByTextContent(screen, textMatch) {
    return screen.findByText((_, contentNode) => findTextWithMarkup(contentNode, textMatch));
}
exports.findByTextContent = findByTextContent;
/**
 * Search for *all* texts broken up by multiple html elements
 * e.g.: <div><div>Hello <span>world</span></div><div>Hello <span>world</span></div></div>
 */
function findAllByTextContent(screen, textMatch) {
    return screen.findAllByText((_, contentNode) => findTextWithMarkup(contentNode, textMatch));
}
exports.findAllByTextContent = findAllByTextContent;
//# sourceMappingURL=utils.jsx.map