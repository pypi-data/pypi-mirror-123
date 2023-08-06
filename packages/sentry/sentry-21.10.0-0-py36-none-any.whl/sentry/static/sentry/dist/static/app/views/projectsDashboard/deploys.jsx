Object.defineProperty(exports, "__esModule", { value: true });
exports.TextOverflow = exports.GetStarted = exports.DeployRows = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const textOverflow_1 = (0, tslib_1.__importDefault)(require("app/components/textOverflow"));
exports.TextOverflow = textOverflow_1.default;
const timeSince_1 = (0, tslib_1.__importDefault)(require("app/components/timeSince"));
const version_1 = (0, tslib_1.__importDefault)(require("app/components/version"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const getDynamicText_1 = (0, tslib_1.__importDefault)(require("app/utils/getDynamicText"));
const DEPLOY_COUNT = 2;
const Deploys = ({ project, shorten }) => {
    const flattenedDeploys = Object.entries(project.latestDeploys || {}).map(([environment, value]) => (Object.assign({ environment }, value)));
    const deploys = (flattenedDeploys || [])
        .sort((a, b) => new Date(b.dateFinished).getTime() - new Date(a.dateFinished).getTime())
        .slice(0, DEPLOY_COUNT);
    if (!deploys.length) {
        return <NoDeploys />;
    }
    return (<DeployRows>
      {deploys.map(deploy => (<Deploy key={`${deploy.environment}-${deploy.version}`} deploy={deploy} project={project} shorten={shorten}/>))}
    </DeployRows>);
};
exports.default = Deploys;
const Deploy = ({ deploy, project, shorten }) => (<react_1.Fragment>
    <icons_1.IconReleases size="sm"/>
    <textOverflow_1.default>
      <Environment>{deploy.environment}</Environment>
      <version_1.default version={deploy.version} projectId={project.id} tooltipRawVersion truncate/>
    </textOverflow_1.default>

    <DeployTime>
      {(0, getDynamicText_1.default)({
        fixed: '3 hours ago',
        value: (<timeSince_1.default date={deploy.dateFinished} shorten={shorten ? shorten : false}/>),
    })}
    </DeployTime>
  </react_1.Fragment>);
const NoDeploys = () => (<GetStarted>
    <button_1.default size="small" href="https://docs.sentry.io/product/releases/" external>
      {(0, locale_1.t)('Track Deploys')}
    </button_1.default>
  </GetStarted>);
const DeployContainer = (0, styled_1.default)('div') `
  padding: ${(0, space_1.default)(2)};
  height: 115px;
`;
const DeployRows = (0, styled_1.default)(DeployContainer) `
  display: grid;
  grid-template-columns: 30px 1fr 1fr;
  grid-template-rows: auto;
  grid-column-gap: ${(0, space_1.default)(1)};
  grid-row-gap: ${(0, space_1.default)(1)};
  font-size: ${p => p.theme.fontSizeMedium};
  line-height: 1.2;
`;
exports.DeployRows = DeployRows;
const Environment = (0, styled_1.default)('div') `
  color: ${p => p.theme.textColor};
  margin: 0;
`;
const DeployTime = (0, styled_1.default)('div') `
  color: ${p => p.theme.gray300};
  overflow: hidden;
  text-align: right;
  text-overflow: ellipsis;
`;
const GetStarted = (0, styled_1.default)(DeployContainer) `
  display: flex;
  align-items: center;
  justify-content: center;
`;
exports.GetStarted = GetStarted;
//# sourceMappingURL=deploys.jsx.map