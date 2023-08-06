Object.defineProperty(exports, "__esModule", { value: true });
// Attempts to get a display name from a Component
//
// Use for HoCs
function getDisplayName(WrappedComponent) {
    return WrappedComponent.displayName || WrappedComponent.name || 'Component';
}
exports.default = getDisplayName;
//# sourceMappingURL=getDisplayName.jsx.map