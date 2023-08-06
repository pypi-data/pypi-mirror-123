Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const find_1 = (0, tslib_1.__importDefault)(require("lodash/find"));
const flatMap_1 = (0, tslib_1.__importDefault)(require("lodash/flatMap"));
const constants_1 = require("app/constants");
const locale_1 = require("app/locale");
const formContext_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/formContext"));
const selectField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/selectField"));
class PermissionSelection extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            permissions: this.props.permissions,
        };
        this.onChange = (resource, choice) => {
            const { permissions } = this.state;
            permissions[resource] = choice;
            this.save(permissions);
        };
        this.save = permissions => {
            this.setState({ permissions });
            this.props.onChange(permissions);
            this.context.form.setValue('scopes', this.permissionStateToList());
        };
    }
    /**
     * Converts the "Permission" values held in `state` to a list of raw
     * API scopes we can send to the server. For example:
     *
     *    ['org:read', 'org:write', ...]
     *
     */
    permissionStateToList() {
        const { permissions } = this.state;
        const findResource = r => (0, find_1.default)(constants_1.SENTRY_APP_PERMISSIONS, ['resource', r]);
        return (0, flatMap_1.default)(Object.entries(permissions), ([r, p]) => { var _a, _b, _c; return (_c = (_b = (_a = findResource(r)) === null || _a === void 0 ? void 0 : _a.choices) === null || _b === void 0 ? void 0 : _b[p]) === null || _c === void 0 ? void 0 : _c.scopes; });
    }
    render() {
        const { permissions } = this.state;
        return (<react_1.Fragment>
        {constants_1.SENTRY_APP_PERMISSIONS.map(config => {
                const toChoice = ([value, opt]) => [value, opt.label];
                const choices = Object.entries(config.choices).map(toChoice);
                const value = permissions[config.resource];
                return (<selectField_1.default 
                // These are not real fields we want submitted, so we use
                // `--permission` as a suffix here, then filter these
                // fields out when submitting the form in
                // sentryApplicationDetails.jsx
                name={`${config.resource}--permission`} key={config.resource} choices={choices} help={(0, locale_1.t)(config.help)} label={(0, locale_1.t)(config.label || config.resource)} onChange={this.onChange.bind(this, config.resource)} value={value} defaultValue={value} disabled={this.props.appPublished} disabledReason={(0, locale_1.t)('Cannot update permissions on a published integration')}/>);
            })}
      </react_1.Fragment>);
    }
}
exports.default = PermissionSelection;
PermissionSelection.contextType = formContext_1.default;
//# sourceMappingURL=permissionSelection.jsx.map