Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const utils_1 = require("app/components/quickTrace/utils");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_2 = require("app/views/performance/transactionSummary/utils");
const types_1 = require("./types");
function getUserKnownDataDetails(data, type, event, organization) {
    switch (type) {
        case types_1.TraceKnownDataType.TRACE_ID: {
            const traceId = data.trace_id || '';
            if (!traceId) {
                return undefined;
            }
            if (!organization.features.includes('discover-basic')) {
                return {
                    subject: (0, locale_1.t)('Trace ID'),
                    value: traceId,
                };
            }
            return {
                subject: (0, locale_1.t)('Trace ID'),
                value: (<ButtonWrapper>
            <pre className="val">
              <span className="val-string">{traceId}</span>
            </pre>
            <StyledButton size="xsmall" to={(0, utils_1.generateTraceTarget)(event, organization)}>
              {(0, locale_1.t)('Search by Trace')}
            </StyledButton>
          </ButtonWrapper>),
            };
        }
        case types_1.TraceKnownDataType.SPAN_ID: {
            return {
                subject: (0, locale_1.t)('Span ID'),
                value: data.span_id || '',
            };
        }
        case types_1.TraceKnownDataType.PARENT_SPAN_ID: {
            return {
                subject: (0, locale_1.t)('Parent Span ID'),
                value: data.parent_span_id || '',
            };
        }
        case types_1.TraceKnownDataType.OP_NAME: {
            return {
                subject: (0, locale_1.t)('Operation Name'),
                value: data.op || '',
            };
        }
        case types_1.TraceKnownDataType.STATUS: {
            return {
                subject: (0, locale_1.t)('Status'),
                value: data.status || '',
            };
        }
        case types_1.TraceKnownDataType.TRANSACTION_NAME: {
            const eventTag = event === null || event === void 0 ? void 0 : event.tags.find(tag => {
                return tag.key === 'transaction';
            });
            if (!eventTag || typeof eventTag.value !== 'string') {
                return undefined;
            }
            const transactionName = eventTag.value;
            const to = (0, utils_2.transactionSummaryRouteWithQuery)({
                orgSlug: organization.slug,
                transaction: transactionName,
                projectID: event.projectID,
                query: {},
            });
            if (!organization.features.includes('performance-view')) {
                return {
                    subject: (0, locale_1.t)('Transaction'),
                    value: transactionName,
                };
            }
            return {
                subject: (0, locale_1.t)('Transaction'),
                value: (<ButtonWrapper>
            <pre className="val">
              <span className="val-string">{transactionName}</span>
            </pre>
            <StyledButton size="xsmall" to={to}>
              {(0, locale_1.t)('View Summary')}
            </StyledButton>
          </ButtonWrapper>),
            };
        }
        default:
            return undefined;
    }
}
const ButtonWrapper = (0, styled_1.default)('div') `
  position: relative;
`;
const StyledButton = (0, styled_1.default)(button_1.default) `
  position: absolute;
  top: ${(0, space_1.default)(0.75)};
  right: ${(0, space_1.default)(0.5)};
`;
exports.default = getUserKnownDataDetails;
//# sourceMappingURL=getTraceKnownDataDetails.jsx.map