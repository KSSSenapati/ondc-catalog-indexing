import  "../style/footer.css";

const Footer = () => {
    return(
        <footer className="footer-section" id="footer">
        <div className="container">
            <div className="footer-cta pt-5 pb-5">
                <div className="row">
                    <div className="col-xl-4 col-md-4 mb-30">
                        <div className="single-cta">
                            <i className="fas fa-map-marker-alt"></i>
                            <div className="cta-text">
                                <h4>Find us</h4>
                                <span>Bangalore, India</span>
                            </div>
                        </div>
                    </div>
                    <div className="col-xl-4 col-md-4 mb-30">
                        <div className="single-cta">
                            <i className="fas fa-phone"></i>
                            <div className="cta-text">
                                <h4>Call us</h4>
                                <span>(+91) 7008789055</span>
                            </div>
                        </div>
                    </div>
                    <div className="col-xl-4 col-md-4 mb-30">
                        <div className="single-cta">
                            <i className="far fa-envelope-open"></i>
                            <div className="cta-text">
                                <h4>Mail us</h4>
                                <span>sntnsenapati@gmail.com</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div className="footer-content pt-5 pb-5">
                <div className="row">
                    <div className="col-xl-4 col-lg-4 mb-50">
                        <div className="footer-widget">
                            <div className="footer-logo">
                                <img src={`${process.env.PUBLIC_URL}/assets/cyborg_logo_white.png`} className="img-fluid" alt="logo" />
                            </div>
                            <div className="footer-text">
                                <p>Our team has implemented a robust catalog indexing system featuring Kafka, Storm, and Solr. This architecture ensures scalable, real-time catalog search and retrieval.</p>
                            </div>
                            <div className="footer-social-icon">
                                <span>Follow us</span>
                                <a href="https://www.linkedin.com/in/ksssenapati/"><img src={`${process.env.PUBLIC_URL}/assets/avatar_1.png`} alt="logo"/></a>
                                <a href="https://www.linkedin.com/in/arnab-paikaray/"><img src={`${process.env.PUBLIC_URL}/assets/avatar_2.png`} alt="logo"/></a>
                                <a href="https://www.linkedin.com/in/pradhan-pk/"><img src={`${process.env.PUBLIC_URL}/assets/avatar_3.png`} alt="logo"/></a>
                                <a href="https://www.linkedin.com/in/krishna-kumarr/"><img src={`${process.env.PUBLIC_URL}/assets/avatar_4.png`} alt="logo"/></a>
                            </div>
                        </div>
                    </div>
                    <div className="col-xl-4 col-lg-4 col-md-6 mb-30">
                        <div className="footer-widget">
                            <div className="footer-widget-heading">
                                <h3>Useful Links</h3>
                            </div>
                            <ul>
                                <li><a href="/">Home</a></li>
                                <li><a href="https://github.com/KSSSenapati/ondc-catalog-indexing">Github Repo</a></li>
                                <li><a href="https://drive.google.com/file/d/1UIuCh_y43TytLtmV46IPtmh94HRQ5KrV/view?usp=drive_link">Solution Deck</a></li>
                                <li><a href="https://drive.google.com/file/d/1qwmKf3vgrO4acBAxs7M9E7FtNOTqsr-w/view?usp=drive_link">Solution Demo</a></li>
                            </ul>
                        </div>
                    </div>
                    <div className="col-xl-4 col-lg-4 col-md-6 mb-50">
                        <div className="footer-widget">
                            <div className="footer-widget-heading">
                                <h3>Watch</h3>
                            </div>
                            <div className="footer-text mb-25">
                                <p>Watch our demo in action</p>
                            </div>
                            <iframe src="https://drive.google.com/file/d/1qwmKf3vgrO4acBAxs7M9E7FtNOTqsr-w/preview" title="Demo" allow="autoplay"></iframe>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </footer>
    )
}


export default Footer;