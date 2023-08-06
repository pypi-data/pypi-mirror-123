Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const useOrganization_1 = require("app/utils/useOrganization");
const relayWrapper_1 = (0, tslib_1.__importDefault)(require("./relayWrapper"));
function OrganizationRelay(props) {
    const organization = (0, useOrganization_1.useOrganization)();
    return (<feature_1.default organization={organization} features={['relay']} hookName="feature-disabled:relay">
      <relayWrapper_1.default organization={organization} {...props}/>
    </feature_1.default>);
}
exports.default = OrganizationRelay;
//# sourceMappingURL=index.jsx.map