Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const isFinite_1 = (0, tslib_1.__importDefault)(require("lodash/isFinite"));
const styles_1 = require("app/components/charts/styles");
const utils_1 = require("app/components/events/interfaces/spans/utils");
const utils_2 = require("app/components/performance/waterfall/utils");
const questionTooltip_1 = (0, tslib_1.__importDefault)(require("app/components/questionTooltip"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const event_1 = require("app/types/event");
const OtherOperation = Symbol('Other');
const TOP_N_SPANS = 4;
class OpsBreakdown extends react_1.Component {
    getTransactionEvent() {
        const { event } = this.props;
        if (event.type === 'transaction') {
            return event;
        }
        return undefined;
    }
    generateStats() {
        var _a, _b;
        const { topN, operationNameFilters } = this.props;
        const event = this.getTransactionEvent();
        if (!event) {
            return [];
        }
        const traceContext = (_a = event === null || event === void 0 ? void 0 : event.contexts) === null || _a === void 0 ? void 0 : _a.trace;
        if (!traceContext) {
            return [];
        }
        const spanEntry = event.entries.find((entry) => {
            return entry.type === event_1.EntryType.SPANS;
        });
        let spans = (_b = spanEntry === null || spanEntry === void 0 ? void 0 : spanEntry.data) !== null && _b !== void 0 ? _b : [];
        const rootSpan = {
            op: traceContext.op,
            timestamp: event.endTimestamp,
            start_timestamp: event.startTimestamp,
            trace_id: traceContext.trace_id || '',
            span_id: traceContext.span_id || '',
            data: {},
        };
        spans =
            spans.length > 0
                ? spans
                : // if there are no descendent spans, then use the transaction root span
                    [rootSpan];
        // Filter spans by operation name
        if (operationNameFilters.type === 'active_filter') {
            spans = [...spans, rootSpan];
            spans = spans.filter(span => {
                const operationName = (0, utils_1.getSpanOperation)(span);
                const shouldFilterOut = typeof operationName === 'string' &&
                    !operationNameFilters.operationNames.has(operationName);
                return !shouldFilterOut;
            });
        }
        const operationNameIntervals = spans.reduce((intervals, span) => {
            let startTimestamp = span.start_timestamp;
            let endTimestamp = span.timestamp;
            if (endTimestamp < startTimestamp) {
                // reverse timestamps
                startTimestamp = span.timestamp;
                endTimestamp = span.start_timestamp;
            }
            // invariant: startTimestamp <= endTimestamp
            let operationName = span.op;
            if (typeof operationName !== 'string') {
                // a span with no operation name is considered an 'unknown' op
                operationName = 'unknown';
            }
            const cover = [startTimestamp, endTimestamp];
            const operationNameInterval = intervals[operationName];
            if (!Array.isArray(operationNameInterval)) {
                intervals[operationName] = [cover];
                return intervals;
            }
            operationNameInterval.push(cover);
            intervals[operationName] = mergeInterval(operationNameInterval);
            return intervals;
        }, {});
        const operationNameCoverage = Object.entries(operationNameIntervals).reduce((acc, [operationName, intervals]) => {
            const duration = intervals.reduce((sum, [start, end]) => {
                return sum + Math.abs(end - start);
            }, 0);
            acc[operationName] = duration;
            return acc;
        }, {});
        const sortedOpsBreakdown = Object.entries(operationNameCoverage).sort((first, second) => {
            const firstDuration = first[1];
            const secondDuration = second[1];
            if (firstDuration === secondDuration) {
                return 0;
            }
            if (firstDuration < secondDuration) {
                // sort second before first
                return 1;
            }
            // otherwise, sort first before second
            return -1;
        });
        const breakdown = sortedOpsBreakdown
            .slice(0, topN)
            .map(([operationName, duration]) => {
            return {
                name: operationName,
                // percentage to be recalculated after the ops breakdown group is decided
                percentage: 0,
                totalInterval: duration,
            };
        });
        const other = sortedOpsBreakdown.slice(topN).reduce((accOther, [_operationName, duration]) => {
            accOther.totalInterval += duration;
            return accOther;
        }, {
            name: OtherOperation,
            // percentage to be recalculated after the ops breakdown group is decided
            percentage: 0,
            totalInterval: 0,
        });
        if (other.totalInterval > 0) {
            breakdown.push(other);
        }
        // calculate breakdown total duration
        const total = breakdown.reduce((sum, operationNameGroup) => {
            return sum + operationNameGroup.totalInterval;
        }, 0);
        // recalculate percentage values
        breakdown.forEach(operationNameGroup => {
            operationNameGroup.percentage = operationNameGroup.totalInterval / total;
        });
        return breakdown;
    }
    render() {
        const { hideHeader } = this.props;
        const event = this.getTransactionEvent();
        if (!event) {
            return null;
        }
        const breakdown = this.generateStats();
        const contents = breakdown.map(currOp => {
            const { name, percentage, totalInterval } = currOp;
            const isOther = name === OtherOperation;
            const operationName = typeof name === 'string' ? name : (0, locale_1.t)('Other');
            const durLabel = Math.round(totalInterval * 1000 * 100) / 100;
            const pctLabel = (0, isFinite_1.default)(percentage) ? Math.round(percentage * 100) : '∞';
            const opsColor = (0, utils_2.pickBarColor)(operationName);
            return (<OpsLine key={operationName}>
          <OpsNameContainer>
            <OpsDot style={{ backgroundColor: isOther ? 'transparent' : opsColor }}/>
            <OpsName>{operationName}</OpsName>
          </OpsNameContainer>
          <OpsContent>
            <Dur>{durLabel}ms</Dur>
            <Pct>{pctLabel}%</Pct>
          </OpsContent>
        </OpsLine>);
        });
        if (!hideHeader) {
            return (<StyledBreakdown>
          <styles_1.SectionHeading>
            {(0, locale_1.t)('Operation Breakdown')}
            <questionTooltip_1.default position="top" size="sm" containerDisplayMode="block" title={(0, locale_1.t)('Span durations are summed over the course of an entire transaction. Any overlapping spans are only counted once. Percentages are calculated by dividing the summed span durations by the total of all span durations.')}/>
          </styles_1.SectionHeading>
          {contents}
        </StyledBreakdown>);
        }
        return <StyledBreakdownNoHeader>{contents}</StyledBreakdownNoHeader>;
    }
}
OpsBreakdown.defaultProps = {
    topN: TOP_N_SPANS,
    hideHeader: false,
};
const StyledBreakdown = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeMedium};
  margin-bottom: ${(0, space_1.default)(4)};
`;
const StyledBreakdownNoHeader = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeMedium};
  margin: ${(0, space_1.default)(2)} ${(0, space_1.default)(3)};
`;
const OpsLine = (0, styled_1.default)('div') `
  display: flex;
  justify-content: space-between;
  margin-bottom: ${(0, space_1.default)(0.5)};

  * + * {
    margin-left: ${(0, space_1.default)(0.5)};
  }
`;
const OpsDot = (0, styled_1.default)('div') `
  content: '';
  display: block;
  width: 8px;
  min-width: 8px;
  height: 8px;
  margin-right: ${(0, space_1.default)(1)};
  border-radius: 100%;
`;
const OpsContent = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
`;
const OpsNameContainer = (0, styled_1.default)(OpsContent) `
  overflow: hidden;
`;
const OpsName = (0, styled_1.default)('div') `
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
`;
const Dur = (0, styled_1.default)('div') `
  color: ${p => p.theme.gray300};
  font-variant-numeric: tabular-nums;
`;
const Pct = (0, styled_1.default)('div') `
  min-width: 40px;
  text-align: right;
  font-variant-numeric: tabular-nums;
`;
function mergeInterval(intervals) {
    // sort intervals by start timestamps
    intervals.sort((first, second) => {
        if (first[0] < second[0]) {
            // sort first before second
            return -1;
        }
        if (second[0] < first[0]) {
            // sort second before first
            return 1;
        }
        return 0;
    });
    // array of disjoint intervals
    const merged = [];
    for (const currentInterval of intervals) {
        if (merged.length === 0) {
            merged.push(currentInterval);
            continue;
        }
        const lastInterval = merged[merged.length - 1];
        const lastIntervalEnd = lastInterval[1];
        const [currentIntervalStart, currentIntervalEnd] = currentInterval;
        if (lastIntervalEnd < currentIntervalStart) {
            // if currentInterval does not overlap with lastInterval,
            // then add currentInterval
            merged.push(currentInterval);
            continue;
        }
        // currentInterval and lastInterval overlaps; so we merge these intervals
        // invariant: lastIntervalStart <= currentIntervalStart
        lastInterval[1] = Math.max(lastIntervalEnd, currentIntervalEnd);
    }
    return merged;
}
exports.default = OpsBreakdown;
//# sourceMappingURL=opsBreakdown.jsx.map