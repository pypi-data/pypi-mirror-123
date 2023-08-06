Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const locale_1 = require("app/locale");
const organization_1 = require("app/styles/organization");
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const widgetBuilder_1 = (0, tslib_1.__importDefault)(require("./widgetBuilder"));
function WidgetBuilderContainer(_a) {
    var { organization } = _a, props = (0, tslib_1.__rest)(_a, ["organization"]);
    return (<feature_1.default features={['metrics', 'dashboards-edit']} organization={organization} renderDisabled={() => (<organization_1.PageContent>
          <alert_1.default type="warning">{(0, locale_1.t)("You don't have access to this feature")}</alert_1.default>
        </organization_1.PageContent>)}>
      <widgetBuilder_1.default {...props} organization={organization}/>
    </feature_1.default>);
}
exports.default = (0, withOrganization_1.default)(WidgetBuilderContainer);
//# sourceMappingURL=index.jsx.map