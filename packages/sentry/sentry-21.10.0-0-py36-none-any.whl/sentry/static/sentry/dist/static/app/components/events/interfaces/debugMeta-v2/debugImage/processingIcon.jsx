Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const debugImage_1 = require("app/types/debugImage");
function ProcessingIcon({ status }) {
    switch (status) {
        case debugImage_1.ImageStatus.TIMEOUT:
        case debugImage_1.ImageStatus.FETCHING_FAILED: {
            return (<tooltip_1.default containerDisplayMode="inline-flex" title={(0, locale_1.t)('The debug information file for this image could not be downloaded')}>
          <icons_1.IconWarning color="yellow300" size="xs"/>
        </tooltip_1.default>);
        }
        case debugImage_1.ImageStatus.MALFORMED: {
            return (<tooltip_1.default containerDisplayMode="inline-flex" title={(0, locale_1.t)('The debug information file for this image failed to process')}>
          <icons_1.IconWarning color="yellow300" size="xs"/>
        </tooltip_1.default>);
        }
        case debugImage_1.ImageStatus.MISSING: {
            return (<tooltip_1.default containerDisplayMode="inline-flex" title={(0, locale_1.t)('No debug information could be found in any of the specified sources')}>
          <icons_1.IconWarning color="yellow300" size="xs"/>
        </tooltip_1.default>);
        }
        case debugImage_1.ImageStatus.FOUND: {
            return (<tooltip_1.default containerDisplayMode="inline-flex" title={(0, locale_1.t)('Debug information for this image was found and successfully processed')}>
          <icons_1.IconCheckmark color="green300" size="xs"/>
        </tooltip_1.default>);
        }
        case debugImage_1.ImageStatus.UNUSED: {
            return (<tooltip_1.default containerDisplayMode="inline-flex" title={(0, locale_1.t)('The image was not required for processing the stack trace')}>
          <icons_1.IconInfo color="gray200" size="xs"/>
        </tooltip_1.default>);
        }
        case debugImage_1.ImageStatus.OTHER: {
            return (<tooltip_1.default containerDisplayMode="inline-flex" title={(0, locale_1.t)('An internal error occurred while handling this image')}>
          <icons_1.IconWarning color="yellow300" size="xs"/>
        </tooltip_1.default>);
        }
        default: {
            Sentry.withScope(scope => {
                scope.setLevel(Sentry.Severity.Warning);
                Sentry.captureException(new Error('Unknown image ProcessingIcon status'));
            });
            return null; // This shall not happen
        }
    }
}
exports.default = ProcessingIcon;
//# sourceMappingURL=processingIcon.jsx.map