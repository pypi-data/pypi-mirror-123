Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_lazyload_1 = (0, tslib_1.__importDefault)(require("react-lazyload"));
const miniBarChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/miniBarChart"));
const locale_1 = require("app/locale");
const ProjectStatsGraph = ({ project, stats }) => {
    stats = stats || project.stats || [];
    const series = [
        {
            seriesName: (0, locale_1.t)('Events'),
            data: stats.map(point => ({ name: point[0] * 1000, value: point[1] })),
        },
    ];
    return (<react_1.Fragment>
      {series && (<react_lazyload_1.default height={25} debounce={50}>
          <miniBarChart_1.default isGroupedByDate showTimeInTooltip series={series} height={25}/>
        </react_lazyload_1.default>)}
    </react_1.Fragment>);
};
exports.default = ProjectStatsGraph;
//# sourceMappingURL=projectStatsGraph.jsx.map