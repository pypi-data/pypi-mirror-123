Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const noProjectMessage_1 = (0, tslib_1.__importDefault)(require("app/components/noProjectMessage"));
const sentryDocumentTitle_1 = (0, tslib_1.__importDefault)(require("app/components/sentryDocumentTitle"));
const locale_1 = require("app/locale");
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
function TeamInsightsContainer({ children, organization }) {
    return (<feature_1.default organization={organization} features={['team-insights']}>
      <noProjectMessage_1.default organization={organization}>
        <sentryDocumentTitle_1.default title={(0, locale_1.t)('Project Reports')} orgSlug={organization.slug}>
          {children && (0, react_1.isValidElement)(children)
            ? (0, react_1.cloneElement)(children, {
                organization,
            })
            : children}
        </sentryDocumentTitle_1.default>
      </noProjectMessage_1.default>
    </feature_1.default>);
}
exports.default = (0, withOrganization_1.default)(TeamInsightsContainer);
//# sourceMappingURL=index.jsx.map