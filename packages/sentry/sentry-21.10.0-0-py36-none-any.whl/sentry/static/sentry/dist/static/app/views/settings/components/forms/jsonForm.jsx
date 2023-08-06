Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const scroll_to_element_1 = (0, tslib_1.__importDefault)(require("scroll-to-element"));
const utils_1 = require("app/utils");
const sanitizeQuerySelector_1 = require("app/utils/sanitizeQuerySelector");
const formPanel_1 = (0, tslib_1.__importDefault)(require("./formPanel"));
class JsonForm extends React.Component {
    constructor() {
        var _a;
        super(...arguments);
        this.state = {
            // location.hash is optional because of tests.
            highlighted: (_a = this.props.location) === null || _a === void 0 ? void 0 : _a.hash,
        };
    }
    componentDidMount() {
        this.scrollToHash();
    }
    UNSAFE_componentWillReceiveProps(nextProps) {
        if (this.props.location.hash !== nextProps.location.hash) {
            const hash = nextProps.location.hash;
            this.scrollToHash(hash);
            this.setState({ highlighted: hash });
        }
    }
    scrollToHash(toHash) {
        var _a;
        // location.hash is optional because of tests.
        const hash = toHash || ((_a = this.props.location) === null || _a === void 0 ? void 0 : _a.hash);
        if (!hash) {
            return;
        }
        // Push onto callback queue so it runs after the DOM is updated,
        // this is required when navigating from a different page so that
        // the element is rendered on the page before trying to getElementById.
        try {
            (0, scroll_to_element_1.default)((0, sanitizeQuerySelector_1.sanitizeQuerySelector)(decodeURIComponent(hash)), {
                align: 'middle',
                offset: -100,
            });
        }
        catch (err) {
            Sentry.captureException(err);
        }
    }
    shouldDisplayForm(fields) {
        const fieldsWithVisibleProp = fields.filter(field => typeof field !== 'function' && (0, utils_1.defined)(field === null || field === void 0 ? void 0 : field.visible));
        if (fields.length === fieldsWithVisibleProp.length) {
            const _a = this.props, { additionalFieldProps } = _a, props = (0, tslib_1.__rest)(_a, ["additionalFieldProps"]);
            const areAllFieldsHidden = fieldsWithVisibleProp.every(field => {
                if (typeof field.visible === 'function') {
                    return !field.visible(Object.assign(Object.assign({}, props), additionalFieldProps));
                }
                return !field.visible;
            });
            return !areAllFieldsHidden;
        }
        return true;
    }
    renderForm({ fields, formPanelProps, title, }) {
        const shouldDisplayForm = this.shouldDisplayForm(fields);
        if (!shouldDisplayForm &&
            !(formPanelProps === null || formPanelProps === void 0 ? void 0 : formPanelProps.renderFooter) &&
            !(formPanelProps === null || formPanelProps === void 0 ? void 0 : formPanelProps.renderHeader)) {
            return null;
        }
        return <formPanel_1.default title={title} fields={fields} {...formPanelProps}/>;
    }
    render() {
        const _a = this.props, { access, collapsible, fields, title, forms, disabled, features, additionalFieldProps, renderFooter, renderHeader, location: _location } = _a, otherProps = (0, tslib_1.__rest)(_a, ["access", "collapsible", "fields", "title", "forms", "disabled", "features", "additionalFieldProps", "renderFooter", "renderHeader", "location"]);
        const formPanelProps = {
            access,
            disabled,
            features,
            additionalFieldProps,
            renderFooter,
            renderHeader,
            highlighted: this.state.highlighted,
            collapsible,
        };
        return (<div {...otherProps}>
        {typeof forms !== 'undefined' &&
                forms.map((formGroup, i) => (<React.Fragment key={i}>
              {this.renderForm(Object.assign({ formPanelProps }, formGroup))}
            </React.Fragment>))}
        {typeof forms === 'undefined' &&
                typeof fields !== 'undefined' &&
                this.renderForm({ fields, formPanelProps, title })}
      </div>);
    }
}
exports.default = (0, react_router_1.withRouter)(JsonForm);
//# sourceMappingURL=jsonForm.jsx.map