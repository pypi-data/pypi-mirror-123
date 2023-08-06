Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const indicator_1 = require("app/actionCreators/indicator");
const api_1 = require("app/api");
const locale_1 = require("app/locale");
const form_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/form"));
class ApiForm extends react_1.Component {
    constructor() {
        super(...arguments);
        this.api = new api_1.Client();
        this.onSubmit = (data, onSuccess, onError) => {
            this.props.onSubmit && this.props.onSubmit(data);
            (0, indicator_1.addLoadingMessage)((0, locale_1.t)('Saving changes\u2026'));
            this.api.request(this.props.apiEndpoint, {
                method: this.props.apiMethod,
                data,
                success: response => {
                    (0, indicator_1.clearIndicators)();
                    onSuccess(response);
                },
                error: error => {
                    (0, indicator_1.clearIndicators)();
                    onError(error);
                },
            });
        };
    }
    componentWillUnmount() {
        this.api.clear();
    }
    render() {
        const _a = this.props, { onSubmit: _onSubmit, apiMethod: _apiMethod, apiEndpoint: _apiEndpoint } = _a, otherProps = (0, tslib_1.__rest)(_a, ["onSubmit", "apiMethod", "apiEndpoint"]);
        return <form_1.default onSubmit={this.onSubmit} {...otherProps}/>;
    }
}
exports.default = ApiForm;
//# sourceMappingURL=apiForm.jsx.map