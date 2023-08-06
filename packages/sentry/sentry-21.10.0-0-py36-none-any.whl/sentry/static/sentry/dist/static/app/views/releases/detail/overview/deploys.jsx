Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const deployBadge_1 = (0, tslib_1.__importDefault)(require("app/components/deployBadge"));
const textOverflow_1 = (0, tslib_1.__importDefault)(require("app/components/textOverflow"));
const timeSince_1 = (0, tslib_1.__importDefault)(require("app/components/timeSince"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const styles_1 = require("./styles");
const Deploys = ({ version, orgSlug, projectId, deploys }) => {
    return (<styles_1.Wrapper>
      <styles_1.SectionHeading>{(0, locale_1.t)('Deploys')}</styles_1.SectionHeading>

      {deploys.map(deploy => (<Row key={deploy.id}>
          <StyledDeployBadge deploy={deploy} orgSlug={orgSlug} version={version} projectId={projectId}/>
          <textOverflow_1.default>
            <timeSince_1.default date={deploy.dateFinished}/>
          </textOverflow_1.default>
        </Row>))}
    </styles_1.Wrapper>);
};
const Row = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: ${(0, space_1.default)(1)};
  font-size: ${p => p.theme.fontSizeMedium};
  color: ${p => p.theme.subText};
`;
const StyledDeployBadge = (0, styled_1.default)(deployBadge_1.default) `
  margin-right: ${(0, space_1.default)(1)};
`;
exports.default = Deploys;
//# sourceMappingURL=deploys.jsx.map