Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const isFunction_1 = (0, tslib_1.__importDefault)(require("lodash/isFunction"));
const indicator_1 = require("app/actionCreators/indicator");
const api_1 = require("app/api");
const forms_1 = require("app/components/forms");
const locale_1 = require("app/locale");
const callbackWithArgs = function (context, callback, ...args) {
    return (0, isFunction_1.default)(callback) ? callback.bind(context, ...args) : undefined;
};
class PluginComponentBase extends React.Component {
    constructor(props, context) {
        super(props, context);
        this.api = new api_1.Client();
        [
            'onLoadSuccess',
            'onLoadError',
            'onSave',
            'onSaveSuccess',
            'onSaveError',
            'onSaveComplete',
            'renderField',
        ].map(method => (this[method] = this[method].bind(this)));
        if (this.fetchData) {
            this.fetchData = this.onLoad.bind(this, this.fetchData.bind(this));
        }
        if (this.onSubmit) {
            this.onSubmit = this.onSave.bind(this, this.onSubmit.bind(this));
        }
        this.state = {
            state: forms_1.FormState.READY,
        };
    }
    componentWillUnmount() {
        this.api.clear();
    }
    fetchData() {
        // Allow children to implement this
    }
    onSubmit() {
        // Allow children to implement this
    }
    onLoad(callback, ...args) {
        this.setState({
            state: forms_1.FormState.LOADING,
        }, callbackWithArgs(this, callback, ...args));
    }
    onLoadSuccess() {
        this.setState({
            state: forms_1.FormState.READY,
        });
    }
    onLoadError(callback, ...args) {
        this.setState({
            state: forms_1.FormState.ERROR,
        }, callbackWithArgs(this, callback, ...args));
        (0, indicator_1.addErrorMessage)((0, locale_1.t)('An error occurred.'));
    }
    onSave(callback, ...args) {
        if (this.state.state === forms_1.FormState.SAVING) {
            return;
        }
        callback = callbackWithArgs(this, callback, ...args);
        this.setState({
            state: forms_1.FormState.SAVING,
        }, () => {
            (0, indicator_1.addLoadingMessage)((0, locale_1.t)('Saving changes\u2026'));
            callback && callback();
        });
    }
    onSaveSuccess(callback, ...args) {
        callback = callbackWithArgs(this, callback, ...args);
        this.setState({
            state: forms_1.FormState.READY,
        }, () => callback && callback());
        setTimeout(() => {
            (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Success!'));
        }, 0);
    }
    onSaveError(callback, ...args) {
        callback = callbackWithArgs(this, callback, ...args);
        this.setState({
            state: forms_1.FormState.ERROR,
        }, () => callback && callback());
        setTimeout(() => {
            (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to save changes. Please try again.'));
        }, 0);
    }
    onSaveComplete(callback, ...args) {
        (0, indicator_1.clearIndicators)();
        callback = callbackWithArgs(this, callback, ...args);
        callback && callback();
    }
    renderField(props) {
        var _a;
        props = Object.assign({}, props);
        const newProps = Object.assign(Object.assign({}, props), { formState: this.state.state });
        return <forms_1.GenericField key={(_a = newProps.config) === null || _a === void 0 ? void 0 : _a.name} {...newProps}/>;
    }
}
exports.default = PluginComponentBase;
//# sourceMappingURL=pluginComponentBase.jsx.map