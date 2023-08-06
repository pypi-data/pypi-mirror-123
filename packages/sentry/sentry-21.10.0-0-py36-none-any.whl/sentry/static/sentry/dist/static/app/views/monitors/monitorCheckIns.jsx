Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const duration_1 = (0, tslib_1.__importDefault)(require("app/components/duration"));
const panels_1 = require("app/components/panels");
const timeSince_1 = (0, tslib_1.__importDefault)(require("app/components/timeSince"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const checkInIcon_1 = (0, tslib_1.__importDefault)(require("./checkInIcon"));
class MonitorCheckIns extends asyncComponent_1.default {
    getEndpoints() {
        const { monitor } = this.props;
        return [
            ['checkInList', `/monitors/${monitor.id}/checkins/`, { query: { per_page: 10 } }],
        ];
    }
    renderError() {
        return <ErrorWrapper>{super.renderError()}</ErrorWrapper>;
    }
    renderBody() {
        return (<panels_1.PanelBody>
        {this.state.checkInList.map(checkIn => (<panels_1.PanelItem key={checkIn.id}>
            <CheckInIconWrapper>
              <checkInIcon_1.default status={checkIn.status} size={16}/>
            </CheckInIconWrapper>
            <TimeSinceWrapper>
              <timeSince_1.default date={checkIn.dateCreated}/>
            </TimeSinceWrapper>
            <DurationWrapper>
              {checkIn.duration && <duration_1.default seconds={checkIn.duration / 100}/>}
            </DurationWrapper>
          </panels_1.PanelItem>))}
      </panels_1.PanelBody>);
    }
}
exports.default = MonitorCheckIns;
const DivMargin = (0, styled_1.default)('div') `
  margin-right: ${(0, space_1.default)(2)};
`;
const CheckInIconWrapper = (0, styled_1.default)(DivMargin) `
  display: flex;
  align-items: center;
`;
const TimeSinceWrapper = (0, styled_1.default)(DivMargin) `
  font-variant-numeric: tabular-nums;
`;
const DurationWrapper = (0, styled_1.default)('div') `
  font-variant-numeric: tabular-nums;
`;
const ErrorWrapper = (0, styled_1.default)('div') `
  margin: ${(0, space_1.default)(3)} ${(0, space_1.default)(3)} 0;
`;
//# sourceMappingURL=monitorCheckIns.jsx.map