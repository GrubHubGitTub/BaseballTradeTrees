import Image from "next/image"

export default function Footer() {
    return (
        <div className="footer">
            <div className="footer--buttons">
                <Image src="/github.png" width="38px" height="38px"/>
                <Image src="/reddit.png" width="40px" height="40px"/>
                <Image src="/mail.png" width="40px" height="40px"/>
            </div>   
            <p className="footer--retro">Transaction and player information was obtained free of charge from Retrosheet.</p> 
        </div>
    )
}