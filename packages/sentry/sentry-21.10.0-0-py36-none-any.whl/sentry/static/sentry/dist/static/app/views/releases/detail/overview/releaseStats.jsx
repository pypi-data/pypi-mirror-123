Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const styles_1 = require("app/components/charts/styles");
const deployBadge_1 = (0, tslib_1.__importDefault)(require("app/components/deployBadge"));
const notAvailable_1 = (0, tslib_1.__importDefault)(require("app/components/notAvailable"));
const timeSince_1 = (0, tslib_1.__importDefault)(require("app/components/timeSince"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
function ReleaseStats({ organization, release, project }) {
    var _a;
    const { lastDeploy, dateCreated, version } = release;
    return (<Container>
      <div>
        <styles_1.SectionHeading>
          {(lastDeploy === null || lastDeploy === void 0 ? void 0 : lastDeploy.dateFinished) ? (0, locale_1.t)('Date Deployed') : (0, locale_1.t)('Date Created')}
        </styles_1.SectionHeading>
        <div>
          <timeSince_1.default date={(_a = lastDeploy === null || lastDeploy === void 0 ? void 0 : lastDeploy.dateFinished) !== null && _a !== void 0 ? _a : dateCreated}/>
        </div>
      </div>

      <div>
        <styles_1.SectionHeading>{(0, locale_1.t)('Last Deploy')}</styles_1.SectionHeading>
        <div>
          {(lastDeploy === null || lastDeploy === void 0 ? void 0 : lastDeploy.dateFinished) ? (<deployBadge_1.default deploy={lastDeploy} orgSlug={organization.slug} version={version} projectId={project.id}/>) : (<notAvailable_1.default />)}
        </div>
      </div>
    </Container>);
}
const Container = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: 50% 50%;
  grid-row-gap: ${(0, space_1.default)(2)};
  margin-bottom: ${(0, space_1.default)(3)};
`;
exports.default = ReleaseStats;
//# sourceMappingURL=releaseStats.jsx.map