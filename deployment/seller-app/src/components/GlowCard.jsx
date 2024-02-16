const GlowCard = ({title, description, buttonFunction, icon}) => {
    return (
        
        <div className='glow-card'>
            <div className='face face1'>
                <div class="glow-content">
                    <i class={icon}></i>
                    <h3>{title}</h3>
                </div>
            </div>
            <div class="face face2">
                <div class="glow-content">
                    <p> {description}</p>
                    <a onClick={buttonFunction} type='button'> {title} </a>
                </div>
            </div>
        </div>
    )
}

export default GlowCard;