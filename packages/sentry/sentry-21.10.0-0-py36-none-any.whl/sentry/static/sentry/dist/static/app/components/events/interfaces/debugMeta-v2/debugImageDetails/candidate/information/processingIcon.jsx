Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const debugImage_1 = require("app/types/debugImage");
function ProcessingIcon({ processingInfo }) {
    switch (processingInfo.status) {
        case debugImage_1.CandidateProcessingStatus.OK:
            return <icons_1.IconCheckmark color="green300" size="xs"/>;
        case debugImage_1.CandidateProcessingStatus.ERROR: {
            const { details } = processingInfo;
            return (<tooltip_1.default title={details} disabled={!details}>
          <icons_1.IconClose color="red300" size="xs"/>
        </tooltip_1.default>);
        }
        case debugImage_1.CandidateProcessingStatus.MALFORMED: {
            const { details } = processingInfo;
            return (<tooltip_1.default title={details} disabled={!details}>
          <icons_1.IconWarning color="yellow300" size="xs"/>
        </tooltip_1.default>);
        }
        default: {
            Sentry.withScope(scope => {
                scope.setLevel(Sentry.Severity.Warning);
                Sentry.captureException(new Error('Unknown image candidate ProcessingIcon status'));
            });
            return null; // this shall never happen
        }
    }
}
exports.default = ProcessingIcon;
//# sourceMappingURL=processingIcon.jsx.map