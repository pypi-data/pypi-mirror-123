Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const featureDisabled_1 = (0, tslib_1.__importDefault)(require("app/components/acl/featureDisabled"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const groupEventAttachments_1 = (0, tslib_1.__importDefault)(require("./groupEventAttachments"));
const GroupEventAttachmentsContainer = ({ organization, group }) => (<feature_1.default features={['event-attachments']} organization={organization} renderDisabled={props => <featureDisabled_1.default {...props}/>}>
    <groupEventAttachments_1.default projectSlug={group.project.slug}/>
  </feature_1.default>);
exports.default = (0, withOrganization_1.default)(GroupEventAttachmentsContainer);
//# sourceMappingURL=index.jsx.map