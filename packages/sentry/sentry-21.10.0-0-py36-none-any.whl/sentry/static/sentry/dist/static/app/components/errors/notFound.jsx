Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const NotFound = () => (<NotFoundAlert type="error" icon={<icons_1.IconInfo size="lg"/>}>
    <Heading>{(0, locale_1.t)('Page Not Found')}</Heading>
    <p>{(0, locale_1.t)('The page you are looking for was not found.')}</p>
    <p>{(0, locale_1.t)('You may wish to try the following:')}</p>
    <ul>
      <li>
        {(0, locale_1.t)(`If you entered the address manually, double check the path. Did you
           forget a trailing slash?`)}
      </li>
      <li>
        {(0, locale_1.t)(`If you followed a link here, try hitting back and reloading the
           page. It's possible the resource was moved out from under you.`)}
      </li>
      <li>
        {(0, locale_1.tct)('If all else fails, [link:contact us] with more details', {
        link: (<externalLink_1.default href="https://github.com/getsentry/sentry/issues/new/choose"/>),
    })}
      </li>
    </ul>
    <p>
      {(0, locale_1.tct)('Not sure what to do? [link:Return to the dashboard]', {
        link: <link_1.default to="/"/>,
    })}
    </p>
  </NotFoundAlert>);
const NotFoundAlert = (0, styled_1.default)(alert_1.default) `
  margin: ${(0, space_1.default)(3)} 0;
`;
const Heading = (0, styled_1.default)('h1') `
  font-size: ${p => p.theme.fontSizeExtraLarge};
  margin: ${(0, space_1.default)(1)} 0;
`;
exports.default = NotFound;
//# sourceMappingURL=notFound.jsx.map