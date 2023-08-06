Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const pick_1 = (0, tslib_1.__importDefault)(require("lodash/pick"));
const moment_1 = (0, tslib_1.__importDefault)(require("moment"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const count_1 = (0, tslib_1.__importDefault)(require("app/components/count"));
const getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
const globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
const locale_1 = require("app/locale");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/utils");
const utils_2 = require("../../utils");
const styles_1 = require("./styles");
class TotalCrashFreeUsers extends asyncComponent_1.default {
    constructor() {
        super(...arguments);
        this.shouldReload = true;
    }
    getEndpoints() {
        const { location, organization, projectSlug, version } = this.props;
        return [
            [
                'releaseStats',
                `/projects/${organization.slug}/${projectSlug}/releases/${version}/stats/`,
                {
                    query: Object.assign(Object.assign({}, (0, getParams_1.getParams)((0, pick_1.default)(location.query, [globalSelectionHeader_1.URL_PARAM.PROJECT, globalSelectionHeader_1.URL_PARAM.ENVIRONMENT]))), { type: 'sessions' }),
                },
            ],
        ];
    }
    componentDidUpdate(prevProps) {
        if (prevProps.version !== this.props.version) {
            this.remountComponent();
        }
    }
    renderLoading() {
        return this.renderBody();
    }
    renderBody() {
        var _a;
        const crashFreeTimeBreakdown = (_a = this.state.releaseStats) === null || _a === void 0 ? void 0 : _a.usersBreakdown;
        if (!(crashFreeTimeBreakdown === null || crashFreeTimeBreakdown === void 0 ? void 0 : crashFreeTimeBreakdown.length)) {
            return null;
        }
        const timeline = crashFreeTimeBreakdown
            .map(({ date, crashFreeUsers, totalUsers }, index, data) => {
            // count number of crash free users from knowing percent and total
            const crashFreeUserCount = Math.round(((crashFreeUsers !== null && crashFreeUsers !== void 0 ? crashFreeUsers : 0) * totalUsers) / 100);
            // first item of timeline is release creation date, then we want to have relative date label
            const dateLabel = index === 0
                ? (0, locale_1.t)('Release created')
                : `${(0, moment_1.default)(data[0].date).from(date, true)} ${(0, locale_1.t)('later')}`;
            return { date: (0, moment_1.default)(date), dateLabel, crashFreeUsers, crashFreeUserCount };
        })
            // remove those timeframes that are in the future
            .filter(item => item.date.isBefore())
            // we want timeline to go from bottom to up
            .reverse();
        if (!timeline.length) {
            return null;
        }
        return (<styles_1.Wrapper>
        <styles_1.SectionHeading>{(0, locale_1.t)('Total Crash Free Users')}</styles_1.SectionHeading>
        <Timeline>
          {timeline.map(row => (<Row key={row.date.toString()}>
              <InnerRow>
                <Text bold>{row.date.format('MMMM D')}</Text>
                <Text bold right>
                  <count_1.default value={row.crashFreeUserCount}/>{' '}
                  {(0, locale_1.tn)('user', 'users', row.crashFreeUserCount)}
                </Text>
              </InnerRow>
              <InnerRow>
                <Text>{row.dateLabel}</Text>
                <Percent right>
                  {(0, utils_1.defined)(row.crashFreeUsers)
                    ? (0, utils_2.displayCrashFreePercent)(row.crashFreeUsers)
                    : '-'}
                </Percent>
              </InnerRow>
            </Row>))}
        </Timeline>
      </styles_1.Wrapper>);
    }
}
const Timeline = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeMedium};
  line-height: 1.2;
`;
const DOT_SIZE = 10;
const Row = (0, styled_1.default)('div') `
  border-left: 1px solid ${p => p.theme.border};
  padding-left: ${(0, space_1.default)(2)};
  padding-bottom: ${(0, space_1.default)(1)};
  margin-left: ${(0, space_1.default)(1)};
  position: relative;

  &:before {
    content: '';
    width: ${DOT_SIZE}px;
    height: ${DOT_SIZE}px;
    border-radius: 100%;
    background-color: ${p => p.theme.purple300};
    position: absolute;
    top: 0;
    left: -${Math.floor(DOT_SIZE / 2)}px;
  }

  &:last-child {
    border-left: 0;
  }
`;
const InnerRow = (0, styled_1.default)('div') `
  display: grid;
  grid-column-gap: ${(0, space_1.default)(2)};
  grid-auto-flow: column;
  grid-auto-columns: 1fr;

  padding-bottom: ${(0, space_1.default)(0.5)};
`;
const Text = (0, styled_1.default)('div') `
  text-align: ${p => (p.right ? 'right' : 'left')};
  color: ${p => (p.bold ? p.theme.textColor : p.theme.gray300)};
  padding-bottom: ${(0, space_1.default)(0.25)};
  ${overflowEllipsis_1.default};
`;
const Percent = (0, styled_1.default)(Text) `
  font-variant-numeric: tabular-nums;
`;
exports.default = TotalCrashFreeUsers;
//# sourceMappingURL=totalCrashFreeUsers.jsx.map