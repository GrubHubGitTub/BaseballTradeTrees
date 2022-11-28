import Image from "next/image"

export default function Footer() {
    return (
        <div className="footer">
            <div className="footer--buttons">
                <a href="https://github.com/GrubHubGitTub/BaseballTradeTrees" target="_blank" rel="noopener noreferrer"><Image src="/github.png" width="38px" height="36px" /></a>
                <a href="https://twitter.com/MLB_TradeTrees" target="_blank" rel="noopener noreferrer"> <Image src="/twitter.png" width="40px" height="40px" /> </a>
                <a href="mailto:baseballtradetrees@gmail.com" target="_blank" rel="noopener noreferrer"><Image src="/mail.png" width="40px" height="40px" /> </a>
            </div>   
            <p className="footer--retro">Transaction and player information was obtained free of charge from Retrosheet.</p> 
        </div>
    )
}