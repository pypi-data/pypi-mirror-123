Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const tagStore_1 = (0, tslib_1.__importDefault)(require("app/stores/tagStore"));
const getDisplayName_1 = (0, tslib_1.__importDefault)(require("app/utils/getDisplayName"));
/**
 * HOC for getting *only* tags from the TagStore.
 */
function withTags(WrappedComponent) {
    class WithTags extends React.Component {
        constructor() {
            super(...arguments);
            this.state = {
                tags: tagStore_1.default.getAllTags(),
            };
            this.unsubscribe = tagStore_1.default.listen((tags) => this.setState({ tags }), undefined);
        }
        componentWillUnmount() {
            this.unsubscribe();
        }
        render() {
            const _a = this.props, { tags } = _a, props = (0, tslib_1.__rest)(_a, ["tags"]);
            return <WrappedComponent {...Object.assign({ tags: tags !== null && tags !== void 0 ? tags : this.state.tags }, props)}/>;
        }
    }
    WithTags.displayName = `withTags(${(0, getDisplayName_1.default)(WrappedComponent)})`;
    return WithTags;
}
exports.default = withTags;
//# sourceMappingURL=withTags.jsx.map