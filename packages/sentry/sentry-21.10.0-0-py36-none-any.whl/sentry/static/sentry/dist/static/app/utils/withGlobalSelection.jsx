Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const globalSelectionStore_1 = (0, tslib_1.__importDefault)(require("app/stores/globalSelectionStore"));
const getDisplayName_1 = (0, tslib_1.__importDefault)(require("app/utils/getDisplayName"));
/**
 * Higher order component that uses GlobalSelectionStore and provides the
 * active project
 */
function withGlobalSelection(WrappedComponent) {
    class WithGlobalSelection extends React.Component {
        constructor() {
            super(...arguments);
            this.state = globalSelectionStore_1.default.get();
            this.unsubscribe = globalSelectionStore_1.default.listen((selection) => {
                if (this.state !== selection) {
                    this.setState(selection);
                }
            }, undefined);
        }
        componentWillUnmount() {
            this.unsubscribe();
        }
        render() {
            const { isReady, selection } = this.state;
            return (<WrappedComponent selection={selection} isGlobalSelectionReady={isReady} {...this.props}/>);
        }
    }
    WithGlobalSelection.displayName = `withGlobalSelection(${(0, getDisplayName_1.default)(WrappedComponent)})`;
    return WithGlobalSelection;
}
exports.default = withGlobalSelection;
//# sourceMappingURL=withGlobalSelection.jsx.map