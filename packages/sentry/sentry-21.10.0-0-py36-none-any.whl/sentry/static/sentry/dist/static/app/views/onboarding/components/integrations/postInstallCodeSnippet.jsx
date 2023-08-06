Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const locale_1 = require("app/locale");
function PostInstallCodeSnippet({ provider, platform, isOnboarding, }) {
    // currently supporting both Python and Node
    const token_punctuation = platform === 'python-awslambda' ? '()' : '();';
    return (<div>
      <p>
        {(0, locale_1.t)("Congrats, you just installed the %s integration! Now that it's is installed, the next time you trigger an error it will go to your Sentry.", provider.name)}
      </p>
      <p>
        {(0, locale_1.t)('This snippet includes an intentional error, so you can test that everything is working as soon as you set it up:')}
      </p>
      <div>
        <CodeWrapper>
          <code>
            <TokenFunction>myUndefinedFunction</TokenFunction>
            <TokenPunctuation>{token_punctuation}</TokenPunctuation>)
          </code>
        </CodeWrapper>
      </div>
      {isOnboarding && (<react_1.Fragment>
          <p>
            {(0, locale_1.t)("If you're new to Sentry, use the email alert to access your account and complete a product tour.")}
          </p>
          <p>
            {(0, locale_1.t)("If you're an existing user and have disabled alerts, you won't receive this email.")}
          </p>
        </react_1.Fragment>)}
    </div>);
}
exports.default = PostInstallCodeSnippet;
const CodeWrapper = (0, styled_1.default)('pre') `
  padding: 1em;
  overflow: auto;
  background: #251f3d;
  font-size: 15px;
`;
const TokenFunction = (0, styled_1.default)('span') `
  color: #7cc5c4;
`;
const TokenPunctuation = (0, styled_1.default)('span') `
  color: #b3acc1;
`;
//# sourceMappingURL=postInstallCodeSnippet.jsx.map