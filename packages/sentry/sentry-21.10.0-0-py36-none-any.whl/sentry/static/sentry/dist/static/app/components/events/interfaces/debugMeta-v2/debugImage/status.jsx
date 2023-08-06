Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const tag_1 = (0, tslib_1.__importDefault)(require("app/components/tag"));
const locale_1 = require("app/locale");
const debugImage_1 = require("app/types/debugImage");
function Status({ status }) {
    switch (status) {
        case debugImage_1.ImageStatus.OTHER:
        case debugImage_1.ImageStatus.FETCHING_FAILED:
        case debugImage_1.ImageStatus.MALFORMED:
        case debugImage_1.ImageStatus.TIMEOUT: {
            return <StyledTag type="error">{(0, locale_1.t)('Error')}</StyledTag>;
        }
        case debugImage_1.ImageStatus.MISSING: {
            return <StyledTag type="error">{(0, locale_1.t)('Missing')}</StyledTag>;
        }
        case debugImage_1.ImageStatus.FOUND: {
            return <StyledTag type="success">{(0, locale_1.t)('Ok')}</StyledTag>;
        }
        case debugImage_1.ImageStatus.UNUSED: {
            return <StyledTag>{(0, locale_1.t)('Unreferenced')}</StyledTag>;
        }
        default: {
            Sentry.withScope(scope => {
                scope.setLevel(Sentry.Severity.Warning);
                Sentry.captureException(new Error('Unknown image status'));
            });
            return <StyledTag>{(0, locale_1.t)('Unknown')}</StyledTag>; // This shall not happen
        }
    }
}
exports.default = Status;
const StyledTag = (0, styled_1.default)(tag_1.default) `
  &,
  span div {
    max-width: 100%;
  }
`;
//# sourceMappingURL=status.jsx.map