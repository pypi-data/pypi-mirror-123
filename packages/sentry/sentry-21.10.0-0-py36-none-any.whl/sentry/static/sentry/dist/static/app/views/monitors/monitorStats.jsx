Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const miniBarChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/miniBarChart"));
const panels_1 = require("app/components/panels");
const locale_1 = require("app/locale");
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
const emptyMessage_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/emptyMessage"));
class MonitorStats extends asyncComponent_1.default {
    getEndpoints() {
        const { monitor } = this.props;
        const until = Math.floor(new Date().getTime() / 1000);
        const since = until - 3600 * 24 * 30;
        return [
            [
                'stats',
                `/monitors/${monitor.id}/stats/`,
                {
                    query: {
                        since,
                        until,
                        resolution: '1d',
                    },
                },
            ],
        ];
    }
    renderBody() {
        var _a;
        let emptyStats = true;
        const success = {
            seriesName: (0, locale_1.t)('Successful'),
            data: [],
        };
        const failed = {
            seriesName: (0, locale_1.t)('Failed'),
            data: [],
        };
        (_a = this.state.stats) === null || _a === void 0 ? void 0 : _a.forEach(p => {
            if (p.ok || p.error) {
                emptyStats = false;
            }
            const timestamp = p.ts * 1000;
            success.data.push({ name: timestamp.toString(), value: p.ok });
            failed.data.push({ name: timestamp.toString(), value: p.error });
        });
        const colors = [theme_1.default.green300, theme_1.default.red300];
        return (<panels_1.Panel>
        <panels_1.PanelBody withPadding>
          {!emptyStats ? (<miniBarChart_1.default isGroupedByDate showTimeInTooltip labelYAxisExtents stacked colors={colors} height={150} series={[success, failed]}/>) : (<emptyMessage_1.default title={(0, locale_1.t)('Nothing recorded in the last 30 days.')} description={(0, locale_1.t)('All check-ins for this monitor.')}/>)}
        </panels_1.PanelBody>
      </panels_1.Panel>);
    }
}
exports.default = MonitorStats;
//# sourceMappingURL=monitorStats.jsx.map