Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const selectAsyncControl_1 = (0, tslib_1.__importDefault)(require("./selectAsyncControl"));
const selectField_1 = (0, tslib_1.__importDefault)(require("./selectField"));
class SelectAsyncField extends selectField_1.default {
    constructor() {
        super(...arguments);
        this.onResults = data => {
            const { name } = this.props;
            const results = data && data[name];
            return (results && results.map(({ id, text }) => ({ value: id, label: text }))) || [];
        };
        this.onQuery = query => 
        // Used by legacy integrations
        ({ autocomplete_query: query, autocomplete_field: this.props.name });
    }
    getField() {
        // Callers should be able to override all props except onChange
        // FormField calls props.onChange via `setValue`
        return (<selectAsyncControl_1.default id={this.getId()} onResults={this.onResults} onQuery={this.onQuery} {...this.props} value={this.state.value} onChange={this.onChange}/>);
    }
}
SelectAsyncField.defaultProps = Object.assign(Object.assign({}, selectField_1.default.defaultProps), { placeholder: 'Start typing to search for an issue' });
exports.default = SelectAsyncField;
//# sourceMappingURL=selectAsyncField.jsx.map