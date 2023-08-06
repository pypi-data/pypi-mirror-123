Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_router_1 = require("react-router");
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const chartZoom_1 = (0, tslib_1.__importDefault)(require("app/components/charts/chartZoom"));
const errorPanel_1 = (0, tslib_1.__importDefault)(require("app/components/charts/errorPanel"));
const lineChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/lineChart"));
const transitionChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/transitionChart"));
const transparentLoadingMask_1 = (0, tslib_1.__importDefault)(require("app/components/charts/transparentLoadingMask"));
const notAvailable_1 = (0, tslib_1.__importDefault)(require("app/components/notAvailable"));
const questionTooltip_1 = (0, tslib_1.__importDefault)(require("app/components/questionTooltip"));
const sidebarSectionTitle_1 = (0, tslib_1.__importDefault)(require("app/components/sidebarSectionTitle"));
const tag_1 = (0, tslib_1.__importDefault)(require("app/components/tag"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const types_1 = require("app/types");
const sessions_1 = require("app/utils/sessions");
const list_1 = require("app/views/releases/list");
const content_1 = require("app/views/releases/list/releaseHealth/content");
const utils_1 = require("../../utils");
const utils_2 = require("../utils");
const styles_1 = require("./styles");
function ReleaseComparisonChart({ release, project, environment, releaseSessions, allSessions, loading, reloading, errored, router, location, }) {
    var _a, _b;
    const theme = (0, react_1.useTheme)();
    const hasUsers = !!(0, sessions_1.getCount)(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, types_1.SessionField.USERS);
    function getSeries() {
        if (!releaseSessions) {
            return [];
        }
        const sessionsMarkLines = (0, utils_2.generateReleaseMarkLines)(release, project, theme, location, {
            hideLabel: true,
            axisIndex: 0,
        });
        const series = [
            ...sessionsMarkLines,
            {
                seriesName: (0, locale_1.t)('Sessions Adopted'),
                connectNulls: true,
                yAxisIndex: 0,
                xAxisIndex: 0,
                data: (0, sessions_1.getAdoptionSeries)(releaseSessions.groups, allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, releaseSessions.intervals, types_1.SessionField.SESSIONS),
            },
        ];
        if (hasUsers) {
            const usersMarkLines = (0, utils_2.generateReleaseMarkLines)(release, project, theme, location, {
                hideLabel: true,
                axisIndex: 1,
            });
            series.push(...usersMarkLines);
            series.push({
                seriesName: (0, locale_1.t)('Users Adopted'),
                connectNulls: true,
                yAxisIndex: 1,
                xAxisIndex: 1,
                data: (0, sessions_1.getAdoptionSeries)(releaseSessions.groups, allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, releaseSessions.intervals, types_1.SessionField.USERS),
            });
        }
        return series;
    }
    const colors = theme.charts.getColorPalette(2);
    const axisLineConfig = {
        scale: true,
        axisLine: {
            show: false,
        },
        axisTick: {
            show: false,
        },
        splitLine: {
            show: false,
        },
        max: 100,
        axisLabel: {
            formatter: (value) => `${value}%`,
            color: theme.chartLabel,
        },
    };
    const chartOptions = {
        height: hasUsers ? 280 : 140,
        grid: [
            {
                top: '40px',
                left: '10px',
                right: '10px',
                height: '100px',
            },
            {
                top: '180px',
                left: '10px',
                right: '10px',
                height: '100px',
            },
        ],
        axisPointer: {
            // Link each x-axis together.
            link: [{ xAxisIndex: [0, 1] }],
        },
        xAxes: Array.from(new Array(2)).map((_i, index) => ({
            gridIndex: index,
            type: 'time',
            show: false,
        })),
        yAxes: [
            Object.assign({ 
                // sessions adopted
                gridIndex: 0 }, axisLineConfig),
            Object.assign({ 
                // users adopted
                gridIndex: 1 }, axisLineConfig),
        ],
        // utc: utc === 'true', //TODO(release-comparison)
        isGroupedByDate: true,
        showTimeInTooltip: true,
        colors: [colors[0], colors[1]],
        tooltip: {
            trigger: 'axis',
            truncate: 80,
            valueFormatter: (value, label) => label && Object.values(utils_2.releaseMarkLinesLabels).includes(label) ? '' : `${value}%`,
            filter: (_, seriesParam) => {
                const { seriesName, axisIndex } = seriesParam;
                // do not display tooltips for "Users Adopted" marklines
                if (axisIndex === 1 &&
                    Object.values(utils_2.releaseMarkLinesLabels).includes(seriesName)) {
                    return false;
                }
                return true;
            },
        },
    };
    const { statsPeriod: period, start, end, utc, } = (0, utils_1.getReleaseParams)({
        location,
        releaseBounds: (0, utils_1.getReleaseBounds)(release),
    });
    const isMobileProject = (0, list_1.isProjectMobileForReleases)(project.platform);
    const adoptionStage = (_b = (_a = release.adoptionStages) === null || _a === void 0 ? void 0 : _a[project.slug]) === null || _b === void 0 ? void 0 : _b.stage;
    const adoptionStageLabel = content_1.ADOPTION_STAGE_LABELS[adoptionStage];
    const multipleEnvironments = environment.length === 0 || environment.length > 1;
    return (<styles_1.Wrapper>
      {isMobileProject && (<feature_1.default features={['release-adoption-stage']}>
          <sidebarSectionTitle_1.default title={(0, locale_1.t)('Adoption Stage')} icon={multipleEnvironments && (<questionTooltip_1.default position="top" title={(0, locale_1.t)('See if a release has low adoption, been adopted by users, or replaced by another release. Select an environment above to view the stage this release is in.')} size="sm"/>)}/>
          {adoptionStageLabel && !multipleEnvironments ? (<div>
              <StyledTooltip title={adoptionStageLabel.tooltipTitle} isHoverable>
                <tag_1.default type={adoptionStageLabel.type}>{adoptionStageLabel.name}</tag_1.default>
              </StyledTooltip>
              <AdoptionEnvironment>
                {(0, locale_1.tct)(`in [environment]`, { environment })}
              </AdoptionEnvironment>
            </div>) : (<NotAvailableWrapper>
              <notAvailable_1.default />
            </NotAvailableWrapper>)}
        </feature_1.default>)}
      <RelativeBox>
        <ChartLabel top="0px">
          <ChartTitle title={(0, locale_1.t)('Sessions Adopted')} icon={<questionTooltip_1.default position="top" title={(0, locale_1.t)('Adoption compares the sessions of a release with the total sessions for this project.')} size="sm"/>}/>
        </ChartLabel>

        {hasUsers && (<ChartLabel top="140px">
            <ChartTitle title={(0, locale_1.t)('Users Adopted')} icon={<questionTooltip_1.default position="top" title={(0, locale_1.t)('Adoption compares the users of a release with the total users for this project.')} size="sm"/>}/>
          </ChartLabel>)}

        {errored ? (<errorPanel_1.default height="280px">
            <icons_1.IconWarning color="gray300" size="lg"/>
          </errorPanel_1.default>) : (<transitionChart_1.default loading={loading} reloading={reloading} height="280px">
            <transparentLoadingMask_1.default visible={reloading}/>
            <chartZoom_1.default router={router} period={period !== null && period !== void 0 ? period : undefined} utc={utc === 'true'} start={start} end={end} usePageDate xAxisIndex={[0, 1]}>
              {zoomRenderProps => (<lineChart_1.default {...chartOptions} {...zoomRenderProps} series={getSeries()}/>)}
            </chartZoom_1.default>
          </transitionChart_1.default>)}
      </RelativeBox>
    </styles_1.Wrapper>);
}
const StyledTooltip = (0, styled_1.default)(tooltip_1.default) `
  margin-bottom: ${(0, space_1.default)(3)};
`;
const NotAvailableWrapper = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  margin-bottom: ${(0, space_1.default)(3)};
`;
const AdoptionEnvironment = (0, styled_1.default)('span') `
  margin-left: ${(0, space_1.default)(0.5)};
  font-size: ${p => p.theme.fontSizeSmall};
`;
const RelativeBox = (0, styled_1.default)('div') `
  position: relative;
`;
const ChartTitle = (0, styled_1.default)(sidebarSectionTitle_1.default) `
  margin: 0;
`;
const ChartLabel = (0, styled_1.default)('div') `
  position: absolute;
  top: ${p => p.top};
  z-index: 1;
  left: 0;
  right: 0;
`;
exports.default = (0, react_router_1.withRouter)(ReleaseComparisonChart);
//# sourceMappingURL=releaseAdoption.jsx.map