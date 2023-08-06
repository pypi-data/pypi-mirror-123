Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const utils_1 = require("app/components/organizations/globalSelectionHeader/utils");
const locale_1 = require("app/locale");
const ProjectLink = ({ orgSlug, releaseVersion, project, location }) => (<button_1.default size="xsmall" to={{
        pathname: `/organizations/${orgSlug}/releases/${encodeURIComponent(releaseVersion)}/`,
        query: Object.assign(Object.assign({}, (0, utils_1.extractSelectionParameters)(location.query)), { project: project.id, yAxis: undefined }),
    }}>
    {(0, locale_1.t)('View')}
  </button_1.default>);
exports.default = ProjectLink;
//# sourceMappingURL=projectLink.jsx.map