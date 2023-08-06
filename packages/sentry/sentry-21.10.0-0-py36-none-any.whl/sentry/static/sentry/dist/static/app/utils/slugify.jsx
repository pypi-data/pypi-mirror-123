Object.defineProperty(exports, "__esModule", { value: true });
// XXX: This is NOT an exhaustive slugify function
// Only forces lowercase and replaces spaces with hyphens
function slugify(str) {
    return typeof str === 'string' ? str.toLowerCase().replace(' ', '-') : '';
}
exports.default = slugify;
//# sourceMappingURL=slugify.jsx.map